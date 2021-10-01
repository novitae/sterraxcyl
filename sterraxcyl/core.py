#sterraxcyl v1.2.0 - Oct. 1 2021 https://github.com/novitae/sterraxcyl

import json, os, time, re, csv
import argparse, openpyxl, requests
from stringcolor import *
from tqdm import tqdm
from datetime import datetime, date
from instaloader import instaloader

def MakeExcel(instructions): #Teableau excel de base
    def fileInfos(x):
        ExcelSheet.cell(row = 1, column = x, value = 'S T E R R A X C Y L')
        ExcelSheet.cell(row = 2, column = x, value = '=HYPERLINK("{}", "{}")'.format('https://github.com/novitae', '** Made By novitae **')).style='Hyperlink'
        ExcelSheet.cell(row = 4, column = x, value = 'Targeted account :')
        ExcelSheet.cell(row = 5, column = x, value = '=HYPERLINK("https://www.instagram.com/{}/", "{}")'.format(instructions[0], instructions[0])).style='Hyperlink'
        ExcelSheet.cell(row = 6, column = x, value = 'List :')
        ExcelSheet.cell(row = 7, column = x, value = instructions[1])
        ExcelSheet.cell(row = 9, column = x, value = 'Date :')
        ExcelSheet.cell(row = 10, column = x, value = date.today().strftime("%b-%d-%Y")+datetime.now().strftime(" %H:%M"))
    
    ExcelFile = openpyxl.Workbook()
    ExcelSheet = ExcelFile[ExcelFile.sheetnames[0]]
    ExcelSheet.cell(row = 1, column = 1, value = 'ID')
    ExcelSheet.cell(row = 1, column = 2, value = 'Username')
    ExcelSheet.cell(row = 1, column = 3, value = 'FullName')
    ExcelSheet.cell(row = 1, column = 4, value = 'Page')
    ExcelSheet.cell(row = 1, column = 5, value = 'Biography')
    ExcelSheet.cell(row = 1, column = 6, value = 'IsPrivate')
    ExcelSheet.cell(row = 1, column = 7, value = 'Followers')
    ExcelSheet.cell(row = 1, column = 8, value = 'Following')
    ExcelSheet.cell(row = 1, column = 9, value = 'Posts')
    ExcelSheet.cell(row = 1, column = 10, value = 'External Link')
    ExcelSheet.cell(row = 1, column = 11, value = 'IsBusiness')
    ExcelSheet.cell(row = 1, column = 12, value = 'IsProfessional')
    ExcelSheet.cell(row = 1, column = 13, value = 'IsVerified')
    if instructions[7]:
        ExcelSheet.cell(row = 1, column = 14, value = 'Business Adress')
        ExcelSheet.cell(row = 1, column = 15, value = 'Business Category')
        ExcelSheet.cell(row = 1, column = 16, value = 'Business Contact Method')
        ExcelSheet.cell(row = 1, column = 17, value = 'Business Email')
        ExcelSheet.cell(row = 1, column = 18, value = 'Business Phone Number')
        ExcelSheet.cell(row = 1, column = 19, value = 'Connected Facebook Page')
        ExcelSheet.cell(row = 1, column = 20, value = 'Mutual Followed By')
        ExcelSheet.cell(row = 1, column = 21, value = 'Has Effects')
        ExcelSheet.cell(row = 1, column = 22, value = 'Has Channel')
        ExcelSheet.cell(row = 1, column = 23, value = 'Has Clips')
        ExcelSheet.cell(row = 1, column = 24, value = 'Has Guide')
        ExcelSheet.cell(row = 1, column = 25, value = 'Hide Like and View Count')
        ExcelSheet.cell(row = 1, column = 26, value = 'Has joined Recently')
        fileInfos(27)
    else:
        fileInfos(14)
    ExcelFile.save(instructions[2]+instructions[0].replace('.', '_')+'_'+instructions[1]+'.xlsx')

def ExportExcel(instructions, InfoList, rowN):
    fileName = instructions[2]+instructions[0].replace('.', '_')+'_'+instructions[1]+'.xlsx'
    ExcelFile = openpyxl.load_workbook(filename = fileName)
    ExcelSheet = ExcelFile[ExcelFile.sheetnames[0]]
    ExcelSheet.cell(row = rowN, column = 1, value = int(InfoList[5]))
    ExcelSheet.cell(row = rowN, column = 2, value = InfoList[10])
    ExcelSheet.cell(row = rowN, column = 3, value = InfoList[4])
    ExcelSheet.cell(row = rowN, column = 4, value = '=HYPERLINK("{}", "{}")'.format('https://www.instagram.com/{}/'.format(InfoList[10]), "Account")).style='Hyperlink'
    ExcelSheet.cell(row = rowN, column = 5, value = InfoList[0])
    ExcelSheet.cell(row = rowN, column = 6, value = InfoList[8])
    ExcelSheet.cell(row = rowN, column = 7, value = int(InfoList[2]))
    ExcelSheet.cell(row = rowN, column = 8, value = int(InfoList[3]))
    ExcelSheet.cell(row = rowN, column = 9, value = int(InfoList[11]))
    if InfoList[1] == None:
        pass
    else:
        ExcelSheet.cell(row = rowN, column = 10, value = '=HYPERLINK("{}", "{}")'.format(InfoList[1], InfoList[1])).style='Hyperlink'
    ExcelSheet.cell(row = rowN, column = 11, value = InfoList[6])
    ExcelSheet.cell(row = rowN, column = 12, value = InfoList[7])
    ExcelSheet.cell(row = rowN, column = 13, value = InfoList[9])
    if instructions[7]:
        ExcelSheet.cell(row = rowN, column = 14, value = InfoList[12])
        ExcelSheet.cell(row = rowN, column = 15, value = InfoList[13])
        ExcelSheet.cell(row = rowN, column = 16, value = InfoList[14])
        ExcelSheet.cell(row = rowN, column = 17, value = InfoList[15])
        ExcelSheet.cell(row = rowN, column = 18, value = InfoList[16])
        if InfoList[17] == None:
            pass
        else:
            ExcelSheet.cell(row = rowN, column = 19, value = '=HYPERLINK("{}", "{}")'.format(InfoList[17], InfoList[17])).style='Hyperlink'
        ExcelSheet.cell(row = rowN, column = 20, value = InfoList[18])
        ExcelSheet.cell(row = rowN, column = 21, value = InfoList[19])
        ExcelSheet.cell(row = rowN, column = 22, value = InfoList[20])
        ExcelSheet.cell(row = rowN, column = 23, value = InfoList[21])
        ExcelSheet.cell(row = rowN, column = 24, value = InfoList[22])
        ExcelSheet.cell(row = rowN, column = 25, value = InfoList[23])
        ExcelSheet.cell(row = rowN, column = 26, value = InfoList[24])
    
    ExcelFile.save(fileName)

def MakeCSV(instructions):
    fieldnames = []
    global writer
    if instructions[7]:
        fieldnames = ['ID', 'Username', 'FullName', 'Page', 'Biography', 'IsPrivate', 'Followers', 'Following', 'Posts', 'External Link', 'IsBusiness', 'IsProfessional', 'IsVerified', 'Business Adress', 'Business Category', 'Business Contact Method', 'Business Email', 'Business Phone Number', 'Connected Facebook Page', 'Mutual Followed By', 'Has Effects', 'Has Channel', 'Has Clips', 'Has Guide', 'Hide Like and View Count', 'Has joined Recently']
    else:
        fieldnames = ['ID', 'Username', 'FullName', 'Page', 'Biography', 'IsPrivate', 'Followers', 'Following', 'Posts', 'External Link', 'IsBusiness', 'IsProfessional', 'IsVerified']
    writer = csv.DictWriter(open(instructions[2]+instructions[0].replace('.', '_')+'_'+instructions[1]+'.csv', 'w', newline=''), fieldnames = fieldnames)
    writer.writeheader()

def ExportCSV(instructions, InfoList, rowN):
    if instructions[7]:
        writer.writerow({'ID': InfoList[5], 'Username': InfoList[10], 'FullName': InfoList[4], 'Page': "https://www.instagram.com/{}/".format(instructions[0]), 'Biography': InfoList[0], 'IsPrivate': InfoList[8], 'Followers': InfoList[2], 'Following': InfoList[3], 'Posts': InfoList[11], 'External Link': InfoList[1], 'IsBusiness': InfoList[6], 'IsProfessional': InfoList[7], 'IsVerified': InfoList[9], 'Business Adress': InfoList[12], 'Business Category': InfoList[13], 'Business Contact Method': InfoList[14], 'Business Email': InfoList[15], 'Business Phone Number': InfoList[16], 'Connected Facebook Page': InfoList[17], 'Mutual Followed By': InfoList[18], 'Has Effects': InfoList[19], 'Has Channel': InfoList[20], 'Has Clips': InfoList[21], 'Has Guide': InfoList[22], 'Hide Like and View Count': InfoList[23], 'Has joined Recently': InfoList[24]})
    else:
        writer.writerow({'ID': InfoList[5], 'Username': InfoList[10], 'FullName': InfoList[4], 'Page': "https://www.instagram.com/{}/".format(instructions[0]), 'Biography': InfoList[0], 'IsPrivate': InfoList[8], 'Followers': InfoList[2], 'Following': InfoList[3], 'Posts': InfoList[11], 'External Link': InfoList[1], 'IsBusiness': InfoList[6], 'IsProfessional': InfoList[7], 'IsVerified': InfoList[9]})

def ConvertInfos(instructions, I, rowN):
    try:
        I = I["graphql"]["user"]
    except KeyError:
        if I['spam']:
            print('[{}] Instagram noticed a suspicious activity.\nWe advise you to change of account, and to use delays between your requests with "-d" arg.'.format(cs('!', 'Red3')))
            exit()
    Biography = I["biography"]
    Link = I["external_url"]
    Followers = I["edge_followed_by"]["count"]
    Follows = I["edge_follow"]["count"]
    FullName = I["full_name"]
    Id = I["id"]
    IsBusiness = I["is_business_account"]
    IsProfessional = I["is_professional_account"]
    IsPrivate = I["is_private"]
    IsVerified = I["is_verified"]
    Username = I["username"]
    Posts = I["edge_owner_to_timeline_media"]["count"]
    if instructions[7]:
        BAdress = I["business_address_json"]
        BCategory = I["business_category_name"]
        BContactMethod = I["business_contact_method"]
        BEmail = I["business_email"]
        BPhone = I["business_phone_number"]
        CFacebook = I["connected_fb_page"]
        MutualFollowedBy = I["edge_mutual_followed_by"]["count"]
        HasAREffect = I["has_ar_effects"]
        HasChannel = I["has_channel"]
        HasClips = I["has_clips"]
        HasGuide = I["has_guides"]
        HideLAndV = I["hide_like_and_view_counts"]
        JoinedRecently = I["is_joined_recently"]
        InfoList = [Biography, Link, Followers, Follows, FullName, Id, IsBusiness, IsProfessional, IsPrivate, IsVerified, Username, Posts, BAdress, BCategory, BContactMethod, BEmail, BPhone, CFacebook, MutualFollowedBy, HasAREffect, HasChannel, HasClips, HasGuide, HideLAndV, JoinedRecently]
    else:
        #           0          1     2          3        4         5   6           7               8          9           10        11     12       13         14              15      16      17         18                19           20          21        22        23         24
        InfoList = [Biography, Link, Followers, Follows, FullName, Id, IsBusiness, IsProfessional, IsPrivate, IsVerified, Username, Posts]
    if instructions[9]:
        ExportCSV(instructions, InfoList, rowN)
    else:
        ExportExcel(instructions, InfoList, rowN)

def GetInfoPage(instructions, FollList):
    if instructions[9]:
        MakeCSV(instructions)
    else:
        MakeExcel(instructions)
    rowN = 1 #Ligne à partir de laquelle on écrit les données (+1 ligne ajoutée à ce compte)
    Progression = tqdm(FollList)
    Progression.set_description("{} {} of each {} of the list ".format(instructions[6][3], bold('Getting infos'),instructions[1]))
    for F in Progression: #Pour chaques nom d'utilisateur dans la liste d'utilisateur qui suit / suivit
        time.sleep(instructions[3])
        InfoPage = requests.get('https://www.instagram.com/{}/channel/?__a=1'.format(F),headers = {'User-Agent': instructions[5], 'Referer': 'https://www.instagram.com/'}, cookies = instructions[4])
        InfoPage = json.loads(InfoPage.text)
        rowN += 1
        ConvertInfos(instructions, InfoPage, rowN)

def GetLists(instructions): #On récupère les listes abonnés/abonnements visés
    TargetName = instaloader.Profile.from_username(instructions[8].context, instructions[0]) #On vise le compte ciblé
    FollList = []
    if instructions[1] == 'followers':
        print('{} Extracting followers list of {} profile'.format(instructions[6][0], bold(instructions[0])))
        TargetList = TargetName.get_followers() #on recupère les followers
    elif instructions[1] == 'following':
        print('{} Extracting following list of {} profile'.format(instructions[6][0], bold(instructions[0])))
        TargetList = TargetName.get_followees() #on récupère les followings
    for F in TargetList:
        FollList.append(F.username) #on ajoute chaques compte suivi / qui suit à la liste FollList
    GetInfoPage(instructions, FollList) #on envoi FollList à GetInfo pour retirer les infos des ces comptes

def Target(instructions):
    def exportPrint(instructions):
        if instructions[9]:
            print('{} csv '.format(instructions[6][4])+instructions[1]+' of '+bold(instructions[0])+' succesfully exported in "'+bold(instructions[2])+'" directory, under "'+bold(instructions[0].replace('.', '_')+'_'+instructions[1]+'.csv"'))
        else:
            print('{} xlsx '.format(instructions[6][1])+instructions[1]+' of '+bold(instructions[0])+' succesfully exported in "'+bold(instructions[2])+'" directory, under "'+bold(instructions[0].replace('.', '_')+'_'+instructions[1]+'.xlsx"'))

    if instructions[3] != None:
        print(cs('(', 'Black')+bold('D').cs('Black2', 'White')+cs(')', 'Black')+' Delay between detailed infos requests set to {} seconds'.format(instructions[3]))
    elif instructions[3] == None:
        instructions[3] = 0
    if instructions[1] != 'both':
        GetLists(instructions) #Envoi de la liste choisie
        exportPrint(instructions)
    else: #si les deux listes sont choisies
        instructions[1] = 'followers' #On prends les followers
        GetLists(instructions)
        exportPrint(instructions)
        instructions[1] = 'following' #puis les followings
        GetLists(instructions)
        exportPrint(instructions)
        instructions[1] = 'both' #puis on remet comme avant

def Login(instructions):
    try:
        if os.path.exists(instructions[2]) == False:
            os.mkdir(instructions[2])
        print(' {} logging ... '.format(instructions[6][2]), end='\r')
        identifiants = open(instructions[2]+'identifiants.json', 'r') #Charge les informations de connections
        id = json.load(identifiants)
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        payload = {'username': id['username'],  'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:'+id['password'], 'queryParams': {}, 'optIntoOneTap': 'false' }

        with requests.Session() as s:
            s.headers = {'user-agent': instructions[5]}
            s.headers.update({"Referer": link})
            r = s.get(link)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
            r = s.post(login_url, data = payload, headers = {'user-agent': instructions[5], 'x-requested-with': 'XMLHttpRequest', 'referer': 'https://www.instagram.com/accounts/login/', 'x-csrftoken': csrf })

            if str(r.status_code) == '200':
                reponseData = json.loads(r.text)
                if reponseData['user'] and reponseData['authenticated'] and reponseData['status'] == 'ok': #connecté
                    instructions[4] = r.cookies.get_dict() #ajout des cookies dans instructions
                    instructions[8].login(id['username'], id['password']) #Se connecte avec instaloader
                    print('                       ', end='\r')
                    print('{} Succesfully logged on {} instagram account !'.format(instructions[6][2], bold(id["username"])))
                    Target(instructions)
                    time.sleep(1)
                    s.close()
                    print('{} Closed requests session'.format(instructions[6][0]))
                elif reponseData['user'] == False: #username pas valide
                    print('[{}] Wrong username !'.format(cs('!', 'Red3')))
                elif reponseData['authenticated'] == False: #pas authentifié
                    print('[{}] Not authentificated !'.format(cs('!', 'Red3')))
                else:
                    print('[{}] Unknown error, here is the response:\n'.format(cs('!', 'Red3'))+reponseData)
            else:
                print('[{}] Unknown error, here is the response:\n'.format(cs('!', 'Red3'))+r.text)

    except FileNotFoundError:
        username = input('['+cs('?', 'Violet')+'] Enter an instagram username == >> ')
        password = input('['+cs('?', 'Violet')+'] Enter its password == >> ')
        credentials = open(instructions[2]+'/identifiants.json', 'w')
        credentials.write(json.dumps({'username': username, 'password': password}))
        credentials.close()
        print('{} Credentials are stored in "identifiants.json", in the "{}" directory.'.format(instructions[6][0], bold(instructions[2])))
        Login(instructions)

def main():
    igLogo = bold('i').cs('DodgerBlue2', 'Black')+bold('n').cs('SlateBlue2', 'Black')+bold('s').cs('SlateBlue', 'Black')+bold('t').cs('Pink4', 'Black')+bold('a').cs('LightPink3', 'Black')+bold('g').cs('SandyBrown', 'Black')+bold('r').cs('Gold', 'Black')+bold('a').cs('Yellow2', 'Black')+bold('m').cs('Yellow', 'Black')
    exLogo = bold('e').cs('White', 'DarkGreen')+bold('x').cs('White', 'Green4')+bold('c').cs('White', 'Green4')+bold('e').cs('White', 'DarkGreen')+bold('l').cs('White', 'Green4')+bold('.').cs('White', 'DarkGreen')+bold('x').cs('White', 'Green4')+bold('l').cs('White', 'Green4')+bold('s').cs('White', 'Green4')+bold('x').cs('White', 'DarkGreen')

    print('~   ≈  ~ >=>', igLogo, cs('>', 'LightGrey9', 'Black'), bold('S T E R R A X C Y L').cs('LightGrey9', 'Black').underline(), cs('>', 'LightGrey9', 'Black'), exLogo, '<=<  ~   ≈   ~\n  ~   ≈   ~  ≈>', cs('made  By', 'Grey')+'  '+cs('https://github.com/novitae', 'LightSkyBlue2').underline(), '< <≈  ~ ~  ≈   ~')

    logos = [cs('|', 'DeepSkyBlue5')+bold('§').cs('LightGoldenrod2', 'DeepSkyBlue5')+cs('|', 'LightGoldenrod2'), cs('|', 'Green4')+cs('X', 'White', 'Green4')+cs('|', 'Green4'), cs('|', 'LightSalmon2')+cs('o', 'White', 'DeepPink4')+cs('|', 'MediumOrchid'), cs('|', 'Black')+bold('R').cs('Black2', 'White')+cs('|', 'Black'), cs('|', 'Orange')+bold('c').cs('White', 'Orange')+cs('|', 'Orange')]
    #0 python 1 excel 2 insta 3 request 4 csv

    AChoices = ["followers", "following", "both"]
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all-infos', action='store_true', help='will write down the account extra informations that the program originaly ignores')
    parser.add_argument('-c', '--csv', action='store_true', help='export in csv format instead of excel')
    parser.add_argument('-d', '--delay', metavar='D', type=int, help='delay in seconds between detailed infos requests')
    parser.add_argument('-p', '--path', metavar='P', help='folder path where files will be exported and the credentials stored (by default in "sterraxcyl/")')
    parser.add_argument('-t', '--target', metavar='T', choices=AChoices, help='what do you want to export ("followers", "following" or "both")', required=True)
    parser.add_argument('-u', '--username', metavar='U', help='the instagram username of the aimed account', required=True)
    args = parser.parse_args()

    useragent = 'Instagram 206.1.0.30.118 (iPhone; CPU iPhone OS 15 like Mac OS X, fr-fr) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
    instructions = [args.username, args.target, args.path, args.delay, None, useragent, logos, args.all_infos, instaloader.Instaloader(), args.csv]
    #               0              1            2          3           4     5          6      7               8                          9
    if instructions[2] == None:
        instructions[2] = 'sterraxcyl/'
    Login(instructions)

if __name__ == '__main__':
    main()