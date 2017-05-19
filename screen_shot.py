import Quartz.CoreGraphics as CG
import os

def make_screenshot(num, folder=''):
    all_apps = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionAll, CG.kCGNullWindowID)
    tables = []
    for app in all_apps:
        try:
            if "No Limit Hold'em" in app['kCGWindowName']:
                window_name = app['kCGWindowName'].split(' ')
                if window_name[2] == '-':
                    table_name = ''.join([*window_name[:2]])
                    blinds = [x.replace('$', '') for x in window_name[3].split('/')]
                else:
                    table_name = window_name[0]
                    blinds = [x.replace('$', '') for x in window_name[2].split('/')]
                table = {'Name': '-'.join([table_name, str(num), *blinds]) + '.bmp',
                         'ID': app['kCGWindowNumber']}
                tables.append(table)
        except KeyError:
            continue
    for table in tables:
        file_name = os.path.join(os.path.dirname(__file__), 'scr', folder, table['Name'])
        os.system('screencapture -l {} -o {}'.format(table['ID'], file_name))
    try:
        return file_name
    except UnboundLocalError:
        return ''





