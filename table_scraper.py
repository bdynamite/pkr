import screen_shot
from pkr_data import *
import cv2
import numpy as np
import math
import os
from PIL import Image
import pytesseract
import time
import pprint


def recognize_card(card_bmp):
    rgb_im = card_bmp.convert('RGB')
    control = tuple(rgb_im.getpixel(x) == (255, 255, 255) for x in CONTROL_DOTS)
    try:
        card = ''.join([CONTROL_DICT[control], CONTROL_DICT[rgb_im.getpixel((60, 30))]])
    except KeyError:
        if rgb_im.getpixel((60, 45))[0] in range(160, 190):
            card = 'Hide'
        else:
            card = ''
    return card


def find_dealer(scr):
    im = cv2.imread(scr)
    dealer = cv2.imread('dealer.bmp')
    result = cv2.matchTemplate(im,dealer,cv2.TM_CCOEFF_NORMED)
    dealer_coord = np.unravel_index(result.argmax(),result.shape)[::-1]
    dealer_dist = [(i + 1, math.sqrt((dealer_coord[0] - x[0]) ** 2 +
                                     (dealer_coord[1] - x[1]) ** 2)) for i, x in enumerate(PLAYER_DOTS)]
    return sorted(dealer_dist, key=lambda x: x[1])[0][0]


def start_scraping():
    table_bmp = screen_shot.make_screenshot(num=0)
    dealer = find_dealer(table_bmp)
    print(dealer)
    start = False
    num = 1
    while True:
        table_bmp = screen_shot.make_screenshot(num=num)
        new_dealer = find_dealer(table_bmp)
        print(new_dealer)
        if new_dealer != dealer:
            if start:
                table_round.close()
                break
            dealer = new_dealer
            start = True
            table_round = TableRound(dealer, table_bmp)
        else:
            if start:
                time_0 = time.time()
                table_round.update(table_bmp)
                print(time.time() - time_0)
        num += 1


def get_float(img, box):
    value = pytesseract.image_to_string(img.crop(box=box))
    if value != 'All In':
        try:
            value = float(value.split('$')[1].replace(' ', ''))
        except (ValueError, IndexError):
            value = 'Error'
    else:
        value = 0.0
    return value


class TableRound:

    def __init__(self, dealer, table_bmp):
        self.dealer = dealer
        self.__blinds = tuple(map(float, tuple(os.path.splitext(table_bmp)[0].split('/')[-1].split('-')[2:])))
        self.__seats_order = ['seat_' + str(x + 1) for x in range(self.dealer, 9)] + \
                           ['seat_' + str(x + 1) for x in range(self.dealer)]
        phases = ['start', 'preflop', 'flop', 'turn', 'river', 'end']
        self.__phases = iter(phases)
        self.__phase = next(self.__phases)
        focus_cards_boxes = [SEATS_DICT['seat_' + str(dealer)]['cards'], DECK[2], DECK[3], DECK[4]]
        self.__check_phase_dict = dict(zip(phases, focus_cards_boxes))
        self.__deck = []
        funcs = [self.__update_start, self.__update_preflop, self.__update_flop,
                 self.__update_turn, self.__update_river]
        self.__update_dict = dict(zip(phases, funcs))
        self.__stackes = {}
        self.__players_order = []
        self.__players_money_in_pot = []
        self.__players_names = {}
        self.log = dict((x, []) for x in phases[1:5])
        self.winners = []

    def update(self, table_bmp):
        time_0 = time.time()
        img = Image.open(table_bmp)
        self.__check_phase(img)
        self.__update_dict[self.__phase](img)
        print(self.__phase, self.__players_order, self.__players_names)
        print(self.log)
        print(time.time() - time_0)
        if time.time() - time_0 < .5:
            self.__check_names(img)

    def __check_phase(self, img):
        if self.__phase == 'start':
            focus_card = all([recognize_card(img.crop(box=self.__check_phase_dict[self.__phase][x])) for x in range(2)])
        else:
            if self.__phase == 'river':
                focus_card = None
            else:
                focus_card = recognize_card(img.crop(box=self.__check_phase_dict[self.__phase]))
        if focus_card:
            if self.__phase != 'start':
                if self.__phase == 'preflop':
                    self.__deck = [recognize_card(img.crop(box=DECK[x])) for x in range(2)]
                self.__deck.append(focus_card)
                self.__close_phase(img)
            self.__phase = next(self.__phases)

    def __update_start(self, img):
        pass

    def __update_preflop(self, img):
        if not self.__players_order:
            for seat in self.__seats_order:
                if recognize_card(img.crop(box=SEATS_DICT[seat]['cards'][0])):
                    self.__players_order.append(seat)
                    self.__players_names[seat] = ''
            self.__players_money_in_pot = {x: 0 for x in self.__players_order}
            self.__check_blinds(img)
            self.__get_stackes(img)
        else:
            players_actions = self.__get_actions(img, self.__phase)
            self.log[self.__phase] += (players_actions)


    def __update_flop(self, img):
        players_actions = self.__get_actions(img, self.__phase)
        self.log[self.__phase] += (players_actions)

    def __update_turn(self, img):
        players_actions = self.__get_actions(img, self.__phase)
        self.log[self.__phase] += (players_actions)

    def __update_river(self, img):
        players_actions = self.__get_actions(img, self.__phase)
        self.log[self.__phase] += (players_actions)

    def __check_blinds(self, img):
        rgb_im = img.convert('RGB')
        list_of_extra_bb = [(x, 'BB', self.__blinds[1]) for x in self.__players_order[2:]
                            if not rgb_im.getpixel(SEATS_DICT[x]['bet_dot'])[0] in range(10, 20)]
        self.log['preflop'].extend([(self.__players_order[0], 'SB', self.__blinds[0]),
                                   (self.__players_order[1], 'BB', self.__blinds[1]),
                                   *list_of_extra_bb])

    def __get_stackes(self, img):
        self.__stackes = {x: get_float(img, SEATS_DICT[x]['stack']) for x in self.__players_order}
        self.__stackes[self.__players_order[0]] = round(self.__stackes[self.__players_order[0]] + self.__blinds[0], 2)
        self.__players_money_in_pot[self.__players_order[0]] = self.__blinds[0]
        for bb in self.log['preflop'][1:]:
            self.__stackes[bb[0]] = round(self.__stackes[bb[0]] + bb[2], 2)
            self.__players_money_in_pot[bb[0]] = self.__blinds[1]

    def __get_actions(self, img, phase):
        if self.log[phase]:
            last_player = list(filter(lambda x: x[1] != 'Fold', self.log[phase]))[-1][0]
            last_player_index = self.__players_order.index(last_player)
            players_order_for_this_actions = self.__players_order[last_player_index + 1:] \
                                             + self.__players_order[:last_player_index + 1]
        else:
            players_order_for_this_actions = self.__players_order
        actions = []
        for player in players_order_for_this_actions:
            if player in [x[0] for x in actions]:
                continue
            if len(self.__players_order) == 1:
                if player not in self.winners:
                    self.winners.append(player)
                break
            if not recognize_card(img.crop(box=SEATS_DICT[player]['cards'][0])):
                # fold
                actions.append((player, 'Fold', 0.0))
                self.__players_order.remove(player)
                continue
            all_player_bets = self.__players_money_in_pot[player]
            if all_player_bets == self.__stackes[player]:
                # all-in in some prev phase
                continue
            stack = get_float(img, SEATS_DICT[player]['stack'])
            if round(stack + all_player_bets, 2) == self.__stackes[player]:
                # check or think
                if not self.log[phase]:
                    rgb_im = img.convert('RGB')
                    players_bet_areas = [(x, rgb_im.getpixel(SEATS_DICT[x]['bet_dot'])[0] not in range(10, 20))
                                         for x in players_order_for_this_actions]
                    if any([x[1] for x in players_bet_areas]):
                        for area in players_bet_areas:
                            if area[1]:
                                break
                            actions.append([area[0], 'Check', 0.0])
                    continue
                break
            bet = round(self.__stackes[player] - stack - all_player_bets, 2)
            the_biggest_bet = max(self.__players_money_in_pot.values())
            if round(bet + all_player_bets, 2) <= the_biggest_bet:
                # call or bet or all-in
                actions.append((player, 'Call', bet))
            else:
                if stack:
                    actions.append((player, 'Raise', bet))
                else:
                    actions.append((player, 'All In', bet))
            self.__players_money_in_pot[player] = round(self.__players_money_in_pot[player] + bet, 2)
        return actions

    def __close_phase(self, img):
        if not self.log[self.__phase]:
            self.log[self.__phase] = [(x, 'Check', 0.0) for x in self.__players_order]
            return
        the_biggest_bet = max(self.__players_money_in_pot.values())
        for player in self.__players_order:
            if self.__players_money_in_pot[player] != the_biggest_bet:

                if recognize_card(img.crop(box=SEATS_DICT[player]['cards'][0])):
                    # call
                    stack = get_float(img, SEATS_DICT[player]['stack'])
                    all_player_bets = self.__players_money_in_pot[player]
                    bet = round(self.__stackes[player] - stack - all_player_bets, 2)
                    self.log[self.__phase].append((player, 'Call', bet))
                    self.__players_money_in_pot[player] = round(self.__players_money_in_pot[player] + bet, 2)
                else:
                    # fold
                    self.log[self.__phase].append((player, 'Fold', 0.0))
                    self.__players_order.remove(player)

    def __check_names(self, img):
        noname_players = list(filter(lambda x: not x[1], self.__players_names.items()))
        if noname_players:
            name = pytesseract.image_to_string(img.crop(box=SEATS_DICT[noname_players[0][0]]['name']))
            if name not in BAD_NAMES:
                self.__players_names[noname_players[0][0]] = name

    def close(self):
        pprint.pprint(self.log)


start_scraping()




