PLAYER_DOTS = ((816, 151), (1075, 244), (1057, 432),
               (995, 625), (701, 695), (324, 625),
               (171, 432), (242, 244), (502, 150))
DECK = ((436, 319, 516, 385),
        (527, 319, 607, 385),
        (618, 319, 698, 385),
        (709, 319, 789, 385),
        (800, 319, 880, 385))
CONTROL_DOTS = ((20, 13), (10, 20), (30, 20), (15, 30), (10, 40), (30, 40), (20, 46))
CONTROL_DICT = {(True, False, False, True, True, True, False): 'A',
                (False, True, False, True, True, True, False): 'K',
                (True, False, True, False, True, True, True): 'Q',
                (False, False, True, False, True, True, True): 'J',
                (True, True, False, True, True, False, True): 'T',
                (True, True, True, True, False, True, True): '9',
                (True, True, True, True, True, True, True): '8',
                (True, False, True, False, False, False, False): '7',
                (True, True, False, True, True, True, True): '6',
                (True, True, False, False, True, True, True): '5',
                (True, False, True, False, False, True, False): '4',
                (True, True, True, False, True, True, True): '3',
                (True, True, True, False, True, False, True): '2',
                (66, 94, 103): 'd',
                (76, 116, 50): 'c',
                (58, 58, 58): 's',
                (120, 46, 46): 'h'}
POT_BOX = (520, 270, 800, 300)
SEATS_DICT = {'seat_1': {'name': (817, 121, 964, 147),
                         'stack': (820, 155, 959, 182),
                         'cards': ((773, 50, 853, 103),
                                   (855, 50, 935, 103)),
                         'bet_dot': (811, 231)},
              'seat_2': {'name': (1076, 214, 1223, 240),
                         'stack': (1079, 248, 1218, 275),
                         'cards': ((1033, 144, 1113, 197),
                                   (1114, 144, 1194, 197)),
                         'bet_dot': (961, 283)},
              'seat_3': {'name': (1149, 402, 1296, 428),
                         'stack': (1152, 436, 1291, 463),
                         'cards': ((1105, 332, 1185, 385),
                                  (1187, 332, 1267, 385)),
                         'bet_dot': (1032, 450)},
              'seat_4': {'name': (996, 595, 1143, 621),
                         'stack': (999, 629, 1138, 656),
                         'cards': ((953, 515, 1033, 568),
                                   (1034, 515, 1114, 568)),
                         'bet_dot': (926, 523)},
              'seat_5': {'name': (555, 666, 701, 693),
                         'stack': (560, 699, 697, 724),
                         'cards': ((577, 585, 657, 638),
                                   (658, 585, 738, 638)),
                         'bet_dot': (622, 541)},
              'seat_6': {'name': (178, 596, 324, 623),
                         'stack': (183, 629, 320, 654),
                         'cards': ((200, 515, 280, 568),
                                   (281, 515, 361, 568)),
                         'bet_dot': (402, 522)},
              'seat_7': {'name': (25, 403, 171, 430),
                         'stack': (30, 436, 167, 461),
                         'cards': ((47, 332, 127, 385),
                                   (128, 332, 208, 385)),
                         'bet_dot': (288, 450)},
              'seat_8': {'name': (96, 215, 242, 242),
                         'stack': (101, 248, 238, 273),
                         'cards': ((118, 144, 198, 197),
                                   (199, 144, 279, 197)),
                         'bet_dot': (360, 278)},
              'seat_9': {'name': (356, 121, 502, 148),
                         'stack': (361, 154, 498, 179),
                         'cards': ((378, 50, 458, 103),
                                   (459, 50, 539, 103)),
                         'bet_dot': (529, 249)}}
BAD_NAMES = ('Post BB', 'Post SB', 'Fold', 'Check', 'Raise')
































