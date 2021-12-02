import sys
import os
import argparse

from sterra import _exp
from sterra import _pri
from sterra import _con
from sterra import _ins

from stringcolor import *

def main():
    DP = os.path.dirname(__file__)+'/export/'
    if not os.path.exists(DP):
        os.mkdir(DP)
    if not os.path.exists(DP+'parts/'):
        os.mkdir(DP+'parts/')

    def d():
        print(underline(bold('Please choose a module from the followings:')))
        e = cs('-> ', 'Red2')
        print(f'''    {e}export   (Export list of followers / following / mutuals of an instagram account)
    {e}analyse  (Obtain probabilities for each accounts of being personnal accounts)
    {e}compare  (Shows accounts present in first list and not in the second)
    {e}history  (Check the historic containing all the path of the file you exported, in case you forgot it)
    {e}convert  (Convert a file already exported to another format)
    Don't hesitate to check the WIKI: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md''')
        exit()
    try:
        b = sys.argv[1].lower()
    except IndexError:
        d()

    try:
        print(_pri.logo(b))
    except KeyError:
        pass

    if b == 'export':
        try:
            if sys.argv[2].lower() == 'file':
                export = argparse.ArgumentParser()
                handle1 = export.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: export
                handle2 = export.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: file

                export.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], help='format of the export, by default "excel"')
                export.add_argument('--parts', nargs=(1 or 2), help='path(s) to the complete file(s)')
                export.add_argument('-t', '--target', choices=["followers", "following", "both", "mutuals"], help='what do you want to export ("followers", "following", "both" or "mutuals")', required=True)
                export.add_argument('-p', '--path', metavar='P', help='directory path where export the files (by default in your module path)')
                exargs = export.parse_args()

                exargs.format = "excel" if exargs.format is None else exargs.format
                exargs.path = DP if exargs.path is None else exargs.path
                logo = _pri.Excel() if exargs.format == 'excel' else _pri.CSV() if exargs.format == 'csv' else _pri.Json()
                if not os.path.exists(exargs.path):
                    os.mkdir(exargs.path)

                def make_the_job(path):
                    print(f'{_pri.i()}Conversion ...')
                    j = [_ins.traction.keep_essential_data(False, E) for E in _con.verter(path)]
                    i = _con.getnameinfos(path)
                    return j, i

                if exargs.target == 'followers' or exargs.target == 'following':
                    j, infos = make_the_job(exargs.parts[0])
                    _exp.ort(j, exargs.path, exargs.format, exargs.target, infos['username']).d()
                else:
                    if len(exargs.parts) != 2:
                        _pri.outExcept(e='Argument --parts require two part lists (following and followers)')                
                    
                    l1, i1 = make_the_job(exargs.parts[0])
                    l2, i2 = make_the_job(exargs.parts[1])
                    if exargs.target == 'mutuals':
                        mutuals = _ins.makemutuals(l1, l2)
                        _exp.ort(mutuals, exargs.path, exargs.format, exargs.target).d()
                    
                    else:
                        followers = l1 if i1['type'] == 'followers' else l2
                        following = l2 if i2['type'] == 'following' else l1

                        _exp.ort(followers, exargs.path, exargs.format, exargs.target)
                        _exp.ort(following, exargs.path, exargs.format, exargs.target)
            else:
                raise IndexError
        
        except IndexError:
            export = argparse.ArgumentParser(add_help=False, usage='sterra (-u/--username U | -id ID) -t/--target {followers,following,both,mutuals} (-lcrd/--login-credentials U P | -ssid/--login-session-id S) [--all-infos] -f/--format {excel,csv,json} [-l/--local | -p/--path P] [-d/--delay DELAY | -e/--express] [-h/--help] [--part "PATH_TO_PART"]\n\nWiki: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#export')
            handle = export.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: export

            # TARGET & TARGETLIST
            required = export.add_argument_group(title='required arguments')
            rexclued = required.add_mutually_exclusive_group(required=True)
            rexclued.add_argument('-u', '--username', metavar='U', help='the instagram username of the aimed account', type=str)
            rexclued.add_argument('-id', metavar='ID', help='the instagram id of the aimed account', type=int)
            required.add_argument('-t', '--target', choices=["followers", "following", "both", "mutuals"], help='what do you want to export ("followers", "following", "both" or "mutuals")', required=True)
            
            # LOGIN
            login = export.add_argument_group(title='login arguments')
            lognn = login.add_mutually_exclusive_group(required=True)
            lognn.add_argument('-lcrd', '--login-credentials', metavar=('U', 'P'), nargs=2, help='login by credentials: USERNAME PASSWORD (be sure to keep a space between them)')
            lognn.add_argument('-ssid', '--login-session-id', metavar='S', help='login by SessionID')
            
            # EXPORT
            exports = export.add_argument_group(title='export arguments')
            exports.add_argument('--all-infos', action='store_true', help='writes down the account extra informations that the program originaly ignores')
            exports.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], help='format of the export, by default "excel"')
            exports.add_argument('-p', '--path', metavar='P', help='directory path where export the files (by default in your module path)')

            # SPEED
            spdnm = export.add_argument_group(title='speed arguments')
            speed = spdnm.add_mutually_exclusive_group()
            speed.add_argument('-d', '--delay', type=int, help='delay between requests to get accounts informations')
            speed.add_argument('-e', '--express', action='store_true', help='sends ultra fast requests to get the table faster (deactivated if more than 109 total usernames to avoid blocking)')

            # OPTIONAL
            optional = export.add_argument_group(title='optional arguments')
            optional.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
            optional.add_argument('--part', type=str, help='path of the part')

            exargs = export.parse_args()

            # SET DEFAULTS
            exargs.format = "excel" if exargs.format is None else exargs.format
            exargs.express = False if exargs.express is None else exargs.express
            exargs.path = DP if exargs.path is None else exargs.path
            if not os.path.exists(exargs.path):
                print(exargs.path)
                os.mkdir(exargs.path)

            # EXTRACTION PROCESS
            _ins.tagram(
                tu=(exargs.username, 'username') if exargs.id is None else (exargs.id, 'id'),
                cd=exargs.login_credentials if exargs.login_session_id is None else exargs.login_session_id,
                tl=exargs.target,
                pt=exargs.path,
                ex=exargs.express,
                ai=exargs.all_infos,
                fm=exargs.format,
                rm=exargs.part
            )
        
    elif b == 'compare':
        compare = argparse.ArgumentParser(usage='sterra -f1 PATH_TO_FIRST_FILE -f2 PATH_TO_SECOND_FILE [--no-print] [--url] [--common-usernames] [--not-common-usernames] [-e] [-f {excel,csv,json}] [-p EXPORT_PATH]\n\nWiki: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#compare')
        handle = compare.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: compare

        compare.add_argument('-f1', '--file-1', help='path to the first file to compare to the second file', required=True)
        compare.add_argument('-f2', '--file-2', help='path to the second file to compare to the first file', required=True)
        compare.add_argument('-n', '--no-print', action='store_true', help='doesn\'t print results')
        compare.add_argument('-u', '--url', action='store_true', help='instead of printing usernames, printing urls to the accounts')

        want = compare.add_argument_group(title='data to get')
        want.add_argument('--common-usernames', action='store_true', help='shows the commons usernames (compared with instagram id) in lists')
        want.add_argument('--not-common-usernames', action='store_true', help='shows the not commons usernames in lists')

        expt = compare.add_argument_group(title='export data')
        expt.add_argument('-e', '--export', action='store_true', help='exports the data returned')
        expt.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], help='format of the exported file')
        expt.add_argument('-p', '--path', help='path to the exported file')
        cpargs = compare.parse_args()

        cpargs.format = cpargs.format if cpargs.format is not None else 'excel'
        cpargs.path = cpargs.path if cpargs.path is not None else DP

        f1 = _con.verter(cpargs.file_1)
        f2 = _con.verter(cpargs.file_2)

        lag = ['common_usernames', 'not_common_usernames']
        arglist = []
        for i, tf in enumerate(list(vars(cpargs).keys())):
            if tf in lag and list(vars(cpargs).values())[i] is True:
                arglist.append(tf)

        from sterra import _evo
        for arg in arglist:
            data = _evo.lutio(f1, f2, arg).n()
            if not cpargs.no_print:
                print(_pri.compare()+underline(bold(arg.replace('_', ' ').capitalize()+' :')))
                if data == []:
                    print(bold(cs(' >  No '+arg.replace('_', ' ')+' were found.', 'Red4')))
                else:
                    for dc in data:
                        dt = cs('https://www.instagram.com/', 'LightGrey13')+bold(dc['username'])+cs('/', 'LightGrey13') if cpargs.url else dc['username']
                        print(cs(' >  ', 'DeepSkyBlue7').bold()+dt)
        
            if cpargs.export:
                dt = {
                    'not_common_usernames': f'usernames in {cpargs.file_1} but not in {cpargs.file_2}',
                    'common_usernames': f'usernames in {cpargs.file_1} and also in {cpargs.file_2}'
                }
                _exp.ort(
                    ld=data,
                    tp='comparaison',
                    fm=cpargs.format,
                    tu=str(_con.getnameinfos(cpargs.file_1)['username'])+' & '+str(_con.getnameinfos(cpargs.file_2)['username']),
                    pt=cpargs.path,
                    dt=dt[arg]
                    ).d()

            # shows the accounts present in l1 and not in l2

    elif b == 'analyse':
        analyse = argparse.ArgumentParser(usage='-p/--path PATH [-a/--analysis-type {personnal}] [-d/--descending] [-e/--export] [-f/--format] [-i/--ignore-over] [-n/--no-print] [--pctg] [-s/--size] [-u/--url]\n\nWiki: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#analyse')
        handle = analyse.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: analyse
        
        requ = analyse.add_argument_group(title='required arguments')
        requ.add_argument('-p', '--path', help='path to the file to analyse', required=True)
        
        analyse.add_argument('-a', '--analysis-type', choices=['personnal'], help='type of probabilities asked') # BIENTOT "INTERESTS"
        analyse.add_argument('-d', '--descending', action='store_true', help='instead of printing by highest probability, printing by lowest probability')
        analyse.add_argument('-e', '--export', action='store_true', help='export results')
        analyse.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], help='file export format')
        analyse.add_argument('-i', '--ignore-over', help='quantity of followers over wich we consider the account as impossible to be the close circle of the target (default: 10000)', type=int)
        analyse.add_argument('-n', '--no-print', action='store_true', help='doesn\'t print results')
        analyse.add_argument('--pctg', help='percentage under wich we won\'t print results (between 0 and 98)', type=int)
        analyse.add_argument('-s', '--size', help='size of the most probable username list (will be by default the size of the followers/mutuals/following list filled in)', type=int)
        analyse.add_argument('-u', '--url', action='store_true', help='instead of printing the username of the account, prints the url')
        anargs = analyse.parse_args()

        anargs.analysis_type = anargs.analysis_type if anargs.analysis_type is not None else 'personnal'
        anargs.ignore_over = anargs.ignore_over if anargs.ignore_over is not None else 10000
        anargs.pctg = anargs.pctg if anargs.pctg is not None else 0
        anargs.format = anargs.format if anargs.format is not None else 'excel'

        ld = _con.verter(anargs.path)
        from sterra import _pro
        probas = _pro.babilities(ld=ld, pa=anargs.analysis_type, io=anargs.ignore_over, dd=anargs.descending, pt=anargs.pctg, sz=len(ld) if anargs.size is None else anargs.size).d()
        
        if not anargs.no_print:
            def setcolor(i):
                if i > 85: return 'Green3'
                elif i > 80: return 'Green2'
                elif i > 75: return 'Chartreuse2'
                elif i > 70: return 'GreenYellow'
                elif i > 65: return 'Yellow4'
                elif i > 60: return 'Yellow'
                elif i > 55: return 'LightGoldenrod2'
                elif i > 50: return 'Orange'
                elif i > 45: return 'DarkOrange'
                elif i > 40: return 'OrangeRed'
                elif i > 35: return 'Red2'
                elif i > 30: return 'Red3'
                elif i > 25: return 'Red4'
                elif i > 20: return 'DarkRed2'
                else: return 'DarkRed'

            print(_pri.i()+cs.bold(' Probabilities')+' for '+bold(anargs.path)+' accounts of '+bold('being '+anargs.analysis_type+' account')+f' (showing {len(probas)}/{len(ld)}):')
            print(cs.bold(' >>> '+cs('|', 'DarkGreen')+bold('%%%').cs('White', 'DarkGreen')+cs('|', 'DarkGreen')+' = '+cs.bold('Username')))
            if probas == []:
                nn = cs('->', setcolor(30))
                print(f'      !!! {nn} '+bold('empty list'))
            else:
                for e in probas:
                    lineco = setcolor(int(e['%']))
                    print('      '+bold(e['%'])+'%'+cs(' -> ', lineco)+cs((e['username'] if not anargs.url else cs('https://www.instagram.com/', 'LightGrey9')+bold(e['username'])+cs('/', 'LightGrey9')), 'White').underline())

        if anargs.export:
            fo = _con.getnameinfos(anargs.path)
            t = fo['type']
            _exp.ort(ld=probas, tp=f'{t}_{anargs.analysis_type}_probabilities', fm=anargs.format, tu=fo['username'], pt=fo['path']).d()

    elif b == 'history':
        history = argparse.ArgumentParser(usage='sterra history (--all | --match | --clear)\n\nWiki: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#history')
        handle = history.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: history
        
        choice = history.add_mutually_exclusive_group(required=True)
        choice.add_argument('-a', '--all', action='store_true', help='will print chronologically all the exports path saved in the history')
        choic2 = choice.add_mutually_exclusive_group()
        choic2.add_argument('-m', '--match', help='will print all the exports containing the string attached to this arg (can even be .xlsx to print by format)')
        choic2.add_argument('-c', '--clear', action='store_true', help='clear the historic (you can\'t go back after doing it)')
        hiargs = history.parse_args()

        from sterra import _his
        if hiargs.all:
            _his.tory(ll=True)
        elif hiargs.match is not None:
            _his.tory(nm=hiargs.match)
        elif hiargs.clear:
            _his.tory(cl=True)

    elif b == 'convert':
        convert = argparse.ArgumentParser(usage='sterra convert -p/--path PATH -f/--format {excel, csv, json}\n\nWiki: https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#convert')
        handle = convert.add_argument(' ', help=argparse.SUPPRESS) # Avoid => parsers.py: error: unrecognized arguments: convert

        convert.add_argument('-p', '--path', help='path of the file to convert', required=True)
        convert.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], help='format of the convert', required=True)
        coargs = convert.parse_args()

        fo = _con.getnameinfos(coargs.path)
        bold(_exp.ort(ld=_con.verter(coargs.path), tp=fo['type'], fm=coargs.format, tu=fo['username'], pt=fo['path']).d())

    else:
        d()

    print('[ € ] ~['+cs(' BTC ', 'MediumPurple6').bold()+cs('bc1qjdw2hsspdlw7j9j9qn24gnujnk5thdmt6h2kjh', 'DarkSeaGreen9').underline()+cs(' thx <3 ', 'MediumPurple6').bold()+']~ ~ ~ ~')

if __name__ == '__main__':
    main()