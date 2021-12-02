import os
import re
import random
import time
import json
import requests
import asyncio
import aiohttp

from sterra import _exp
from sterra import _log
from sterra import _pri
from sterra import _user

from stringcolor import *
from tqdm import tqdm

def keskonfé(rtn):
    while True:
        kskfé = str(input(_pri.Interrrogation()+f'Instagram blocked our requests during the process.\n    Do you prefer:\n    1 - Continue with what have been extracted,\n    2 - Export what have been exported as a part (https://github.com/novitae/sterraxcyl/blob/main/WIKI.md#optional-arguments-optional),\n    3 - Stop the program.\n    --> '))
        if kskfé == '1':
            return True

        elif kskfé == '2':
            open(part_path, 'w').write(json.dumps(rtn, indent=4))
            print(f'{_pri.Json()}Part merged to '+bold(part_path))
            exit()

        elif kskfé == '3':
            exit()

        else:
            print(_pri.Exception()+f' "{kskfé}" is not a valid answer, please try again.')

class traction:
    def __init__(self, ul, sd, ai=False, xp=False, dl=0) -> list:
        '''- ul: Usernames list
        - sd: Sessionid
        - ai: All infos ( True | False )
        - xp: Express mode ( True | False )
        - dl: Delay'''

        self.ua = _user.agent()
        self.ul = ul
        self.ck = {'sessionid': sd}
        self.ai = ai
        self.xp = xp
        self.dl = dl

    def keep_essential_data(ai, j):
        j = j['graphql']['user']
        accinfo = {
            'id': j['id'],
            'username': j['username'],
            'name': j['full_name'],
            'link': 'https://www.instagram.com/'+j['username']+'/',
            'biography': j['biography'],
            'is_private': j['is_private'],
            'followers': j['edge_followed_by']['count'],
            'following': j['edge_follow']['count'],
            'posts': j['edge_owner_to_timeline_media']['count'],
            'external_url': j['external_url'],
            'is_business_account': j['is_business_account'],
            'is_professional_account': j['is_professional_account'],
            'is_verified': j['is_verified']}
        if ai:
            accinfo['business_address_json'] = j['business_address_json']
            accinfo['business_category_name'] = j['business_category_name']
            accinfo['business_contact_method'] = j['business_contact_method']
            accinfo['business_email'] = j['business_email']
            accinfo['business_phone_number'] = j['business_phone_number']
            accinfo['connected_fb_page'] = j['connected_fb_page']
            accinfo['mutual_followed_by_count'] = j['edge_mutual_followed_by']['count']
            accinfo['has_ar_effects'] = j['has_ar_effects']
            accinfo['has_channel'] = j['has_channel']
            accinfo['has_clips'] = j['has_clips']
            accinfo['has_guides'] = j['has_guides']
            accinfo['hide_like_and_view_counts'] = j['hide_like_and_view_counts']
            accinfo['is_joined_recently'] = j['is_joined_recently']

        return accinfo

    def get_a__1_normal(self, rtn):
        progressbar = tqdm(self.ul, desc=_pri.Requests()+bold('Details extraction '), colour='Black')
        for usrnm in progressbar:
            __a1 = requests.get(f'https://www.instagram.com/{usrnm}/channel/?__a=1', headers = {'User-Agent': self.ua, 'Referer': f'https://www.instagram.com/{usrnm}'}, cookies=self.ck, allow_redirects=False)
            time.sleep(self.dl)
            if __a1.status_code == 200 and __a1.text != {}:
                rtn.append(__a1.json())
            else:
                progressbar.close()
                if keskonfé(rtn):
                    return rtn
        return rtn

    async def get_a__1_express(self, rtn):
        async def fetch(session, url):
            async with session.get(url, headers = {'User-Agent': self.ua, 'Referer': f'https://www.instagram.com/'}, cookies=self.ck, allow_redirects=False) as __a1:
                if __a1.status == 200 and await __a1.text() != {}:
                    progressbar.update(1)
                    rtn.append(await __a1.json())
                else:
                    progressbar.close()
                    if keskonfé(rtn):
                        return rtn
            return rtn

        progressbar = tqdm(self.ul, desc=_pri.Requests()+bold('Details extraction '), colour='Black')
        async with aiohttp.ClientSession() as session:
            requests_corroutines = []
            for usrnm in self.ul:
                requests_corroutines.append(fetch(session, f'https://www.instagram.com/{usrnm}/channel/?__a=1'))
            futures = asyncio.gather(*requests_corroutines)
            await futures
            await session.close()
        
        progressbar.reset()
        progressbar.update(len(self.ul))
        progressbar.close()

        return rtn

    def strt(self, rtn):
        if not self.xp or len(self.ul) > 110:
            if len(self.ul) > 10:
                print(cs('(', 'Plum3')+bold('☇').cs('Plum3')+cs(')', 'Plum3')+' Details extraction '+cs('can take a while', 'White').bold().underline()+'.\n    You are free to '+cs.bold('do something else').underline()+' while the program does its job.')
            jsonlist = traction.get_a__1_normal(self, rtn)
        elif self.xp:
            loop = asyncio.get_event_loop()
            jsonlist = loop.run_until_complete(traction.get_a__1_express(self, rtn))

        return [traction.keep_essential_data(self.ai, j) for j in jsonlist]

followersList = []
followingList = []
probabilities = {}
target_username = []

def id_to_username(i, u, s):
    '''Returns the username from the ID of an account.'''
    j = requests.get(f'https://i.instagram.com/api/v1/users/{i}/info/', headers={'User-Agent': u}, cookies = {'sessionid': s}, allow_redirects=False)
    if j.status_code == 200:
        return j.json()['user']['username']
    elif j.status_code == 404: _pri.outExcept(e=f'TargetException: The target account associated to "{i}" ID does not exist.')
    else: _pri.outExcept(e=f'ResponseException: The API responded {j.status_code}, you might have been blocked.')

def usernameCheck(u, h, s):
    '''Checks the account existence, and returns its id, followers and following count if it exists, else raises a SterraException'''
    __a1 = requests.get(f'https://www.instagram.com/{u}/channel/?__a=1', cookies = {'sessionid': s}, headers={'User-Agent': h}, allow_redirects=False)
    try:
        if __a1.status_code == 302:
            _pri.outExcept(e=f'ResponseException:\n    Check if your filled well your SessionID. If you did, or logged with an Username and Password.')
        elif __a1.status_code == 404 or __a1.json() == {}:
            _pri.outExcept(e=f'TargetException: The target account "{u}" does not exist.')
        elif __a1.status_code == 200 and __a1.json() != {}:
            j = __a1.json()['graphql']['user']
            return {'id': j['id'], 'followers': j['edge_followed_by']['count'], 'following': j['edge_follow']['count']}
        else:
            _pri.outExcept(e=f'ResponseException: Response {__a1.status_code}, you might have been blocked by instagram.\n    You have no other options than waiting or changing of account.')
    except json.decoder.JSONDecodeError:
        _pri.outExcept(e=f'ResponseException: API rate limit reached, wait an hour or try to use another account.')

class get_follow_list:
    '''Retrieve the followers or following list of an instagram account.'''
    def __init__(self, targid, cred=None, target='following',) -> list:
        '''- targid: The instagram username or id of the account to aim for.
        - cred: SessionID in str or list of credentials like so ["username", "password"] of  the instagram account you want to use.
        - target: The list you want to extract, "following", "followers" or "both". It will be "following" by default.'''

        global sssid
        sssid = _log.in_sssid(cred)
        self.sssid = sssid
        self.trget = target
        self.usrgt = _user.agent()
        reco, tpe = targid # RÉCUPÈRE L'USERNAME SI LE COMPTE VISÉ EST UN ID
        self.usrnm = reco if tpe == 'username' else id_to_username(reco, self.usrgt, self.sssid)

        infos = usernameCheck(self.usrnm, self.usrgt, self.sssid)
        self.trgid = infos['id']
        self.infos = {'followersCount': infos['followers'], 'followingCount': infos['following']}
        print(_pri.x()+cs('Target account', 'Red2').underline()+cs.bold(' >>> ')+cs(self.usrnm, 'White', 'Red2').bold()+', '+cs.bold(str(self.infos['followersCount']))+' followers, '+cs.bold(str(self.infos['followingCount']))+' following.')
        
        if self.trget in ['following', 'both', 'mutuals'] and self.infos['followersCount'] == 0:
            _pri.outExcept(e=f'TargetException: Argument "{self.trget}" needs a list longer than 0 following.')
        if self.trget in ['followers', 'both', 'mutuals'] and self.infos['followingCount'] == 0:
            _pri.outExcept(e=f'TargetException: Argument "{self.trget}" needs a list longer than 0 following.')
        target_username.append(self.usrnm)

    def ig_request(hash_id, variables, resolver, cookies, count, sleep_error = 10, tentatives = 3):
        '''This part of code is pasted from https://github.com/tuxity/insta-unfollower/blob/master/insta-unfollower.py, made to retrieve list of following or follower by 25 unity.'''
        has_next_page = True
        tentatives_actuelles = 0
        
        params = {"query_hash": hash_id, "variables": json.dumps(variables)}
        
        bfadd = 0
        fllwExtrct = tqdm(total=int(count), desc=(_pri.Instagram()+(cs.bold('Followers') if hash_id == 'c76146de99bb02f6415203be841dd25a' else cs.bold('Following'))+' extraction '), colour='Black')
        
        while has_next_page and tentatives_actuelles < tentatives:
            resp = requests.get("https://www.instagram.com/graphql/query/", params = params, cookies = cookies)
            respcookies = resp.cookies.get_dict()
            if respcookies == {}:
                fllwExtrct.close()
                _pri.outExcept(e='TargetException: Be sure that you are following the account you are aiming for if it is in private.')
            
            if resp.status_code == 200:
                tentatives_actuelles = 0

                bfadd = len(followersList if hash_id == 'c76146de99bb02f6415203be841dd25a' else followingList)
                has_next_page = resolver(variables, resp.json())
                fllwExtrct.update(len(followersList if hash_id == 'c76146de99bb02f6415203be841dd25a' else followingList) - bfadd)
                if has_next_page:
                    params["variables"] = json.dumps(variables)

            else:
                tentatives_actuelles += 1
                print(_pri.Exception()+f" An error happened, retry {tentatives_actuelles}/{tentatives} ({sleep_error} seconds between each retry).")
                time.sleep(sleep_error)

        fllwExtrct.reset()
        fllwExtrct.update(int(count))
        fllwExtrct.close()
        return tentatives_actuelles < tentatives

    def resolver_followers(variables, data_resp):
        '''This part of code is pasted from https://github.com/tuxity/insta-unfollower/blob/master/insta-unfollower.py, made to ask ig_request for 25 followers at time'''
        data_resp = data_resp["data"]["user"]["edge_followed_by"]
        
        for node in data_resp["edges"]:
            followersList.append(node["node"]["username"])
                
        if data_resp["page_info"]["has_next_page"]:
            variables["after"] = data_resp["page_info"]["end_cursor"]
            return True
        else:
            return False

    def resolver_following(variables, data_resp):
        '''This part of code is pasted from https://github.com/tuxity/insta-unfollower/blob/master/insta-unfollower.py, made to ask ig_request for 25 following at time'''
        data_resp = data_resp["data"]["user"]["edge_follow"]
        
        for item in data_resp["edges"]:
            followingList.append(item["node"]["username"])
                
        if data_resp["page_info"]["has_next_page"]:
            variables["after"] = data_resp["page_info"]["end_cursor"]
            return True
        else:
            return False

    def generate(self):
        '''Returns the list of every follower or/and following (depends on the arg "target"=???) under a dictionnary containing both'''
        cookies = {'sessionid': self.sssid}
        if self.trget == 'followers':
            get_follow_list.ig_request(hash_id="c76146de99bb02f6415203be841dd25a", variables={"id": self.trgid, "first": 50}, resolver=get_follow_list.resolver_followers, cookies = cookies, count=int(self.infos['followersCount']))
        elif self.trget == 'following':
            get_follow_list.ig_request(hash_id="d04b0a864b4b54837c0d870b0e77e076", variables={"id": self.trgid, "first": 50}, resolver=get_follow_list.resolver_following, cookies = cookies, count=int(self.infos['followingCount']))
        elif self.trget == 'both' or self.trget == 'mutuals':
            get_follow_list.ig_request(hash_id="c76146de99bb02f6415203be841dd25a", variables={"id": self.trgid, "first": 50}, resolver=get_follow_list.resolver_followers, cookies = cookies, count=int(self.infos['followersCount']))
            get_follow_list.ig_request(hash_id="d04b0a864b4b54837c0d870b0e77e076", variables={"id": self.trgid, "first": 50}, resolver=get_follow_list.resolver_following, cookies = cookies, count=int(self.infos['followingCount']))

        if followersList == [] and self.trget == 'followers' and int(self.infos['followersCount']) > 0 or followersList == [] and self.trget == 'both' and int(self.infos['followersCount']) > 0:
            _pri.outExcept(e=f'TargetException: Sterra didn\'t retrieve any username from {self.usrnm}\'s followers. Verify that you have access to this account if it is private.')
        if followingList == [] and self.trget == 'following' and int(self.infos['followingCount']) > 0 or followingList == [] and self.trget == 'both' and int(self.infos['followingCount']) > 0:
            _pri.outExcept(e=f'TargetException: Sterra didn\'t retrieve any username from {self.usrnm}\'s following. Verify that you have access to this account if it is private.')

        return (followersList, followingList)

def makemutuals(lufollowing, lufollowers):
    mutualList = []
    mlngliste = lufollowing if len(lufollowing) <= len(lufollowers) else lufollowers
    plngliste = lufollowers if len(lufollowers) >= len(lufollowing) else lufollowing
    for flw in mlngliste: # LISTE DE MUTUELS
        if flw in plngliste:
            mutualList.append(flw)
    return mutualList

def mk_converted(rm, lufollowers, lufollowing):
    converted = []
    if rm is not None:
        try:
            filename = rm.split('/')[-1]
            if not re.match(r'(followers|following|both)#[0-9]{10}\.json', filename):
                _pri.outExcept(e='Not compatible part file')
            infos = filename.split('#')
            '''target username # followers or following # timestamp . json'''
            
            from sterra import _con
            converted = _con.verter(rm)
            lusername = [U['graphql']['user']['username'] for U in converted]
            if infos[0] == 'followers':
                lufollowers = [F for F in lufollowers if not F in lusername]
            elif infos[0] == 'following':
                lufollowing = [F for F in lufollowing if not F in lusername]
            else: # both, removed but we never know
                lufollowers = [F for F in lufollowers if not F in lusername]
                lufollowing = [F for F in lufollowing if not F in lusername]

        except FileNotFoundError:
            _pri.outExcept(e=f'File supposed to be at {rm} has not been found.')

    return {
        'lufollowers': lufollowers,
        'lufollowing': lufollowing,
        'converted': converted
        }

def tagram(tu, cd, tl, pt, ex=False, ai=False, fm='excel', dl=0, rm=None):
    '''- tu: Target's username like this : ("your target username", "username"), or target's ID like this : ("your target id", "id")
    - cd: Credential ; sessionid (in string) or credentials like this : ["username", "password"] (in list)
    - tl: Target list : following - followers - both - mutuals
    - pt: File path
    - ex: Express mode ( Yes = True | No = False)
    - ai: All infos ( Yes = True | No = False)
    - fm: Format of the file to export : excel - csv - json'''
    ll = get_follow_list(targid=tu, cred=cd, target=tl).generate()
    lufollowers, lufollowing = ll

    global part_path
    part_path = rm if rm is not None else os.path.dirname(__file__)+f'/export/parts/{tl}#{int(time.time())}.json'
    
    if rm is not None and tl in ['both', 'mutuals']:
        _pri.outExcept(e='Part function must be targetting followers or following, not both or mutuals')
    mk = mk_converted(rm, lufollowers, lufollowing)

    if tl in ['followers', 'following', 'both']:
        if tl in ['followers', 'both']:
            followers = traction(ul=mk['lufollowers'], sd=sssid, ai=ai, xp=ex, dl=dl).strt([] if tl in ['following', 'both'] else mk['converted'])
            _exp.ort(ld=followers, tp='followers', fm=fm, tu=target_username[0], pt=pt).d()

        if tl in ['following', 'both']:
            following = traction(ul=mk['lufollowing'], sd=sssid, ai=ai, xp=ex, dl=dl).strt([] if tl in ['followers', 'both'] else mk['converted'])
            _exp.ort(ld=following, tp='following', fm=fm, tu=target_username[0], pt=pt).d()

    elif tl == 'mutuals':
        mutualList = makemutuals(lufollowing, lufollowers)
        if mutualList == []:
            _pri.outExcept(e=f'DataException: Sterra did\'nt find any mutual follows accounts on {tu} account.')
        else:
            mutuals = traction(ul=mutualList, sd=sssid, ai=ex, xp=ex, dl=dl).strt()
            _exp.ort(ld=mutuals, tp='mutuals', fm=fm, tu=target_username[0], path=pt).d()
