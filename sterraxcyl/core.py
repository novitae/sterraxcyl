#sterraxcyl v1.3.0 - Oct. 6 2021 - https://github.com/novitae/sterraxcyl

import json, os, time, re
from sterraxcyl import files
import argparse, requests
from stringcolor import *
from tqdm import tqdm
from datetime import datetime
from instaloader import instaloader
L = instaloader.Instaloader()

def GetInfoPage(FollList):
    open(inst['path']+inst['username'].replace('.', '_')+'_'+inst['target']+'.csv', 'w').close()
    if inst['a_csv']: #WRITES THE CULUMN NAMES IN CSV FILE
        if inst['a_allinfos']:
            ColumnName = {'Id': 'ID', 'Username': 'Username', 'FullName': 'FullName', 'Page': 'Page', 'Biography': 'Biography', 'IsPrivate': 'IsPrivate', 'Followers': 'Followers', 'Follows': 'Following', 'Posts': 'Posts', 'Link': 'External Link', 'IsBusiness': 'IsBusiness', 'IsProfessional': 'IsProfessional', 'IsVerified': 'IsVerified', 'BAdress': 'Business Adress', 'BCategory': 'Business Category', 'BContactMethod': 'Business Contact Method', 'BEmail': 'Business Email', 'BPhone': 'Business Phone Number', 'CFacebook': 'Connected Facebook Page', 'MutualFollowedBy': 'Mutual Followed By', 'HasAREffect': 'Has Effects', 'HasChannel': 'Has Channel', 'HasClips': 'Has Clips', 'HasGuide': 'Has Guide', 'HideLAndV': 'Hide Like and View Count', 'JoinedRecently': 'Has Joined Recently'}
        else:
            ColumnName = {'Id': 'ID', 'Username': 'Username', 'FullName': 'FullName', 'Page': 'Page', 'Biography': 'Biography', 'IsPrivate': 'IsPrivate', 'Followers': 'Followers', 'Follows': 'Following', 'Posts': 'Posts', 'Link': 'External Link', 'IsBusiness': 'IsBusiness', 'IsProfessional': 'IsProfessional', 'IsVerified': 'IsVerified'}
        files.ExportCSV(inst, ColumnName)

    else:
        files.MakeExcel(inst)

    def validResp(InfoPage):
        if "'status': 'fail'" in str(InfoPage):
            print(' {} Instagram noticed the spam activity. We advise you to change of account, stop using --express-mode,\n     use delays between your requests with the --delay. Here is the response :\n'.format(inst['logos'][5]))
            print(InfoPage)
            return False
        else:
            return True

    rowN = 1 #Ligne à partir de laquelle on écrit les données (+1 ligne ajoutée à ce compte)

    if inst['a_express'] and len(FollList) > 200: #EXPRESS MODE DEACTIVATED OVER 200 ACCS
        inst['a_express'] = None
        print(' {} Express mode deactivated because the target list is more than 200 usernames. 200 usernames is a limit over wich you have\n     99% chances of getting blocked by instagram with express mode. You might even get blocked before reaching the limit.'.format(inst['logos'][5]))

    if inst['a_express']: #EXPRESS MODE
        from requests_futures import sessions
        with sessions.FuturesSession() as session:
            InfoPages = [session.get('https://www.instagram.com/{}/channel/?__a=1'.format(F), headers = {'User-Agent': inst['useragent'], 'Referer': 'https://www.instagram.com/'}, cookies = inst['cookies']) for F in FollList]

            Progression = tqdm(InfoPages)
            Progression.set_description(" {} {} of each {} of the list ".format(inst['logos'][3], bold('Getting infos'), inst['target']))
            for I in Progression:
                InfoPage = json.loads(I.result().content)
                rowN += 1
                if validResp(InfoPage):
                    files.ConvertInfos(inst, InfoPage, rowN)
                else:
                    exit()

    else: #NORMAL MODE
        Progression = tqdm(FollList)
        Progression.set_description(" {} {} of each {} of the list ".format(inst['logos'][3], bold('Getting infos'), inst['target']))

        for F in Progression: #Pour chaques nom d'utilisateur dans la liste d'utilisateur qui suit / suivit
            time.sleep(inst['delay'])
            InfoPage = requests.get('https://www.instagram.com/{}/channel/?__a=1'.format(F),headers = {'User-Agent': inst['useragent'], 'Referer': 'https://www.instagram.com/'}, cookies = inst['cookies']) #ssl = False ?
            InfoPage = json.loads(InfoPage.text)
            rowN += 1
            if validResp(InfoPage):
                files.ConvertInfos(inst, InfoPage, rowN)
            else:
                exit()


def GetLists(): #On récupère les listes abonnés/abonnements visés
    TargetName = instaloader.Profile.from_username(L.context, inst['username']) #On vise le compte ciblé
    FollList = []
    if inst['target'] == 'followers':
        print(' {} Extracting followers list of {} ...'.format(inst['logos'][0], bold(inst['username'])))
        TargetList = TargetName.get_followers() #on recupère les followers
    elif inst['target'] == 'following':
        print(' {} Extracting following list of {} ...'.format(inst['logos'][0], bold(inst['username'])))
        TargetList = TargetName.get_followees() #on récupère les followings
    for F in TargetList:
        FollList.append(F.username) #on ajoute chaques compte suivi / qui suit à la liste FollList
    print('     Extracted a list of {} {}.'.format(bold(len(FollList)), bold(inst['target'])))
    
    GetInfoPage(FollList)
    

def Target():
    def exportPrint(): #PRINT INFOS SUR LA LISTE EXPORTÉE
        print(' {} {} '.format(inst['logos'][4 if inst['a_csv'] else 1], 'csv' if inst['a_csv'] else 'xlsx')+inst['target']+' of '+bold(inst['username'])+' succesfully exported in "'+bold(inst['path']+(inst['username'].replace('.', '_'))+'_'+inst['target']+('.csv"' if inst['a_csv'] else '.xlsx"')))
    
    if inst['delay'] != 0: #PRINT LE DÉLAI SÉLÉCTIONNÉ
        print(cs(' (', 'Black')+bold('D').cs('Black2', 'White')+cs(')', 'Black')+' Delay between detailed infos requests set to {} seconds'.format(inst['delay']))
    
    if os.path.exists(inst['path']) == False: #CRÉER LE DOSSIER D'EXPORT
        os.mkdir(inst['path'])

    if inst['target'] != 'both': 
        GetLists() #Envoi de la liste choisie
        exportPrint()
    else: #si les deux listes sont choisies
        inst['target'] = 'followers' #On prends les followers
        GetLists()
        exportPrint()
        inst['target'] = 'following' #puis les followings
        GetLists()
        exportPrint()


def Login():
    path = os.path.join(os.path.dirname(__file__), 'identifiants.json')
    err = inst['logos'][5]
    try:
        print(' {} logging ... '.format(inst['logos'][2]), end='\r')
        id = json.load(open(path, 'r'))
        link = 'https://www.instagram.com/accounts/login/'

        payload = {'username': id['username'],  'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:'+id['password'], 'queryParams': {}, 'optIntoOneTap': 'false' }

        with requests.Session() as s:
            s.headers = {'user-agent': inst['useragent']}
            s.headers.update({"Referer": link})
            r = s.get(link)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
            r = s.post('https://www.instagram.com/accounts/login/ajax/', data = payload, headers = {'user-agent': inst['useragent'], 'x-requested-with': 'XMLHttpRequest', 'referer': 'https://www.instagram.com/accounts/login/', 'x-csrftoken': csrf })

            if str(r.status_code) == '200':
                reponseData = json.loads(r.text)
                if reponseData['user'] and reponseData['authenticated'] and reponseData['status'] == 'ok': #connecté
                    inst['cookies'] = r.cookies.get_dict() #ajout des cookies dans inst
                    time.sleep(1)
                    L.login(id['username'], id['password']) #se connecte avec instaloader
                    print('                        ', end='\r')
                    print(' {} Succesfully logged on {} instagram account !'.format(inst['logos'][2], bold(id["username"])))
                    
                    Target()

                    s.close()
                    print(' {} Closed requests session'.format(inst['logos'][0]))

                else:
                    print(' {} Error, here is the response:\n'.format(err)+reponseData)
                    exit()
            else:
                print(' {} Unknown error, here is the response:\n'.format(err)+r.text)
                exit()

    except FileNotFoundError:
        username = input(' {} Enter an instagram username == >> '.format(inst['logos'][6]))
        password = input(' {} Enter its password == >> '.format(inst['logos'][6]))
        credentials = open(path, 'w')
        credentials.write(json.dumps({'username': username, 'password': password}))
        print(' {} Credentials are stored in "{}" file.\n     You can now launch again, it sould work.'.format(inst['logos'][0], bold(path)))
        

def main():
    #LOGO
    igLogo = bold('i').cs('DodgerBlue2', 'Black')+bold('n').cs('SlateBlue2', 'Black')+bold('s').cs('SlateBlue', 'Black')+bold('t').cs('Pink4', 'Black')+bold('a').cs('LightPink3', 'Black')+bold('g').cs('SandyBrown', 'Black')+bold('r').cs('Gold', 'Black')+bold('a').cs('Yellow2', 'Black')+bold('m').cs('Yellow', 'Black')
    exLogo = bold('e').cs('White', 'DarkGreen')+bold('x').cs('White', 'Green4')+bold('c').cs('White', 'Green4')+bold('e').cs('White', 'DarkGreen')+bold('l').cs('White', 'Green4')+bold('.').cs('White', 'DarkGreen')+bold('x').cs('White', 'Green4')+bold('l').cs('White', 'Green4')+bold('s').cs('White', 'Green4')+bold('x').cs('White', 'DarkGreen')
    csLogo = bold('f').cs('White', 'DarkOrange3')+bold('o').cs('White', 'DarkOrange')+bold('l').cs('White', 'Orange2')+bold('l').cs('White', 'DarkOrange3')+bold('o').cs('White', 'OrangeRed')+bold('w').cs('White', 'DarkOrange')+bold('.').cs('White', 'Orange2')+bold('c').cs('White', 'OrangeRed')+bold('s').cs('White', 'DarkOrange3')+bold('v').cs('White', 'DarkOrange')
    print('~ v.1.3 ~ ~ '+exLogo+'  < < <  '+igLogo+'  > > >  '+csLogo+' ~ ~ GPL-3 ~')
    print('~ \\ \\ \\ ~ ~ > > > > > > > > > '+cs('*sterraxcyl', 'SkyBlue2').underline()+' < < < < < < < < < ~ ~ / / / ~')
    print('[ '+bold('*')+' ]\\ \\  '+cs('made by ', 'MediumPurple6')+bold('aet').cs('MediumPurple6')+cs(' $ https://github.com/novitae/sterraxcyl', 'MediumPurple6')+'  / / /  ~')

    #ARGS
    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-a', '--all-infos', action='store_true', help='writes down the account extra informations that the program originaly ignores')
    optional.add_argument('-c', '--csv', action='store_true', help='exports in csv format instead of excel')
    optional.add_argument('-d', '--delay', metavar='D', type=int, help='delay in seconds between detailed infos requests')
    optional.add_argument('-e', '--express-mode', action='store_true', help='sends ultra fast requests to get the table faster; deactivated if more than 200 usernames in lists')
    optional.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show help message and exit')
    optional.add_argument('-p', '--path', metavar='P', help='directory path where export the files (by default in your module path)')
    required.add_argument('-t', '--target', metavar='T', choices=["followers", "following", "both"], help='what do you want to export ("followers", "following" or "both")', required=True)
    required.add_argument('-u', '--username', metavar='U', help='the instagram username of the aimed account', required=True)
    args = parser.parse_args()

    #INFORMATION LIST INITIATION
    global inst
    inst = {
        'username': args.username,
        'target': args.target,
        'path': os.path.join(os.path.dirname(__file__))+'/export/' if args.path == None else args.path,
        'delay': 0 if args.delay == None else args.delay,
        'cookies': None,
        'useragent': 'Instagram 206.1.0.30.118 (iPhone; CPU iPhone OS 15 like Mac OS X, fr-fr) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'logos': [
            cs('|', 'DeepSkyBlue5')+bold('§').cs('LightGoldenrod2', 'DeepSkyBlue5')+cs('|', 'LightGoldenrod2'), #Python     0
            cs('|', 'Green4')+cs('X', 'White', 'Green4')+cs('|', 'Green4'),                                     #Excel      1
            cs('|', 'LightSalmon2')+cs('o', 'White', 'DeepPink4')+cs('|', 'MediumOrchid'),                      #Instagram  2
            cs('|', 'SeaGreen2')+bold('$').cs('White', 'DarkGrey')+cs('|', 'LightSalmon'),                      #Requests   3
            cs('|', 'Orange')+bold('c').cs('White', 'Orange')+cs('|', 'Orange'),                                #CSV        4
            cs('|', 'Red2')+bold('!').cs('White', 'Red2')+cs('|', 'Red2'),                                      #!          5
            cs('|', 'Violet')+bold('?').cs('White', 'Violet')+cs('|', 'Violet'),                                #?          6
            cs('|', 'DarkSeaGreen9')+bold('+').cs('DarkSeaGreen9', 'White')+cs('|', 'DarkSeaGreen9')            #+          7
            ],
        'a_allinfos': True if args.all_infos else False,
        'a_csv': True if args.csv else False,
        'a_express': True if args.express_mode else False
    }

    if os.path.exists(inst['path']) == False:
        os.mkdir(inst['path'])

    Login()

if __name__ == '__main__':
    main()
