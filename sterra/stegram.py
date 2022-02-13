from re import findall, match
from tqdm import tqdm
from time import sleep
import requests
from random import randint, choice
from aiohttp import ClientSession
from datetime import datetime
from json import loads, dumps, decoder
from asyncio import gather, get_event_loop
from stringcolor import *

from sterra._userAgents_ import USER_AGENTS
from sterra._sterrage_ import ENDPOINTS_TEST_LIST
from sterra._outputs_ import LOGOS, _no_colors
from sterra.SterraException import LoginError, RateLimitError, UserNotFoundError, PrivateAccError, NoFollowError, MutualsError

USER_AGENT = choice(USER_AGENTS["safari"])
IOS_UAGENT = choice(USER_AGENTS["ios"])
global _
_ = None

def _credToSessID(creds:list) -> tuple:
    """Returns the sessionid of the credential given"""
    u, p = tuple(creds)

    session = requests.Session()
    session.headers.update({
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Host": "www.instagram.com",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/",
        "User-Agent": USER_AGENT,
        "X-Instagram-AJAX": "7a3a3e64fa87",
        "X-Requested-With": "XMLHttpRequest"
        })

    mainPage = session.get("https://www.instagram.com")
    csrf = findall(r"csrf_token\":\"(.*?)\"", mainPage.text)[0]
    if not csrf:
        return False, "No csrf token found. Wait 1 hour and retry, or change of account."
    
    session.headers.update({"x-csrftoken": csrf})
    sleep(randint(1, 2))

    data = {"username": u, "enc_password": "#PWD_INSTAGRAM_BROWSER:0:{}:{}".format(int(datetime.now().timestamp()), p)}

    postResp = session.post("https://www.instagram.com/accounts/login/ajax/", data=data, allow_redirects=True)
    response_data = postResp.json()

    if "two_factor_required" in response_data:
        _.r(LoginError("Disable 2-factor authentication to login."))
    if "message" in response_data and response_data["message"] == "checkpoint_required":
        _.r(LoginError("Check Instagram app for a security confirmation."))
    try:
        if not response_data["authenticated"]:
            _.r(LoginError("Invalid credentials."))
    except KeyError:
        if response_data["spam"]:
            _.r(RateLimitError())
    else:
        _.p(dumps(response_data,indent=4))
        _.r(LoginError("Unknown error. Please report the upper dictionnary to the issue section of Sterra."))

    return postResp.cookies["sessionid"]

def _idToUsername(i:str,ss:str) -> str or bool:
    """Returns the username associated to the instagram id
    -i: id, -s: sessonid"""
    apiResp = requests.get(f'https://i.instagram.com/api/v1/users/{i}/info/', headers={'User-Agent':IOS_UAGENT}, cookies = {'sessionid':ss}, allow_redirects=False)
    try:
        apiJson = loads(apiResp.text)
        return apiJson['user']['username']
    except decoder.JSONDecodeError:
        return None if apiResp.status_code == 404 else False

def _targListToHashesAndViceV(s:str) -> list:
    """Returns the hashes for the username list to scrape
    - t: target list"""
    repère = {
        "followers":["c76146de99bb02f6415203be841dd25a"],
        "following":["d04b0a864b4b54837c0d870b0e77e076"],
        "both":["c76146de99bb02f6415203be841dd25a","d04b0a864b4b54837c0d870b0e77e076"],
        "mutuals":["c76146de99bb02f6415203be841dd25a","d04b0a864b4b54837c0d870b0e77e076"]
    }
    for k, v in repère.items():
        if s in [k]+v:
            return (k if s in v else v)

class _instagram:
    def __init__(self, o:object, orgtar:str ,**kwargs:dict) -> None:
        global _
        _ = o
        self.original_target = orgtar

        self.default_h = {'User-Agent':USER_AGENT}
        sessionid = kwargs.get("login_session_id")
        if not sessionid:
            sessionid = _credToSessID(kwargs.get("login_credentials"))

        else:
            self._checkSessidFormat(sessionid)
            self._checkvalidSessid({"sessionid":sessionid})
        self.cookies = {"sessionid":sessionid}
        self.used_account = sessionid.split("%")[0]

        username = kwargs.get("username")
        if not username:
            username = _idToUsername(kwargs.get("id"),sessionid)
            if not username:
                _.r((UserNotFoundError("username" if kwargs.get("username") else "id") if username is None else RateLimitError))
        self.username = username
        
        __a1 = requests.get(f'https://www.instagram.com/{username}/channel/?__a=1', cookies=self.cookies, headers={'User-Agent':USER_AGENT}, allow_redirects=False)
        st = __a1.status_code
        if st != 200:
            _.r((UserNotFoundError("username" if kwargs.get("username") else "id") if st == 404 else RateLimitError))
        j = __a1.json()
        if not j:
            _.r(UserNotFoundError("username" if kwargs.get("username") else "id"))
        j = j['graphql']['user']
        self.acc_infos = {'id': j['id'], 'followers': j['edge_followed_by']['count'], 'following': j['edge_follow']['count']}
        self.target_ig_id = self.acc_infos["id"]

        if j['is_private'] and int(j['edge_owner_to_timeline_media']['count']):
            self._verifyPrivAccAccess()

        _.p(f"""Target > {str(bold(self.username))} ({self.acc_infos["followers"]} followers, {self.acc_infos["following"]} following)""",logo="x")

        self.target_list:str = kwargs.get("target") # ["followers", "following", "both", "mutuals"]

        # relger ce truc tu possible express désactivé meme si la seul liste target est courte
        self.delay = kwargs.get("delay") if kwargs.get("delay") else 0.0
        self.all_infos = kwargs.get("all_infos")
        
        self.no_exp_limit = kwargs.get("no_exp_limit")
        self.want_express = kwargs.get("express")
        self.express = self._canExpress()
        
    def __call__(self) -> dict:
        return vars(self)

    def _canExpress(self, lenght:int=None) -> bool or None:
        if self.want_express and self.no_exp_limit:
            return True

        if self.original_target == "followers":
            possible_express = True if self.acc_infos['followers'] < 109 else False
        elif self.original_target == "following":
            possible_express = True if self.acc_infos['following'] < 109 else False
        elif self.original_target == "mutuals":
            if lenght:
                possible_express = True if lenght < 109 else False
            else:
                possible_express = None
        else:
            possible_express = True if (self.acc_infos['followers']+self.acc_infos['following']) < 109 else False

        if possible_express is None:
            return None
        return (True if self.want_express and possible_express else False)

    def _checkSessidFormat(self,s) -> None:
        """Compares the sessionId to a regex and return True if it matches"""
        if not match(r'[0-9]{1,32}%[0-9a-zA-Z]{16}%[0-9A-Z]{3,4}',s):
            _.r(LoginError("Invalid sessid format"))

    def _checkvalidSessid(self,c:dict) -> None:
        """Raises loginError if the sessionId is not working"""
        status = requests.get(f"https://www.instagram.com/{choice(ENDPOINTS_TEST_LIST)}",headers=self.default_h,cookies=c,allow_redirects=False).status_code
        if status != 200:
            _.r(LoginError("Invalid sessid"))

    def _verifyPrivAccAccess(self) -> None:
        """Works only if account has posts"""
        page = requests.get(f"https://www.instagram.com/{self.username}/",headers=self.default_h,cookies=self.cookies,allow_redirects=False).text
        try:
            infos = loads(page.split("<script type=\"text/javascript\">window._sharedData = ")[-1].split(";</script>")[0])["entry_data"]["ProfilePage"][0]["graphql"]["user"]
            if not infos["edge_owner_to_timeline_media"]["edges"]+infos["edge_felix_video_timeline"]["edges"]:
                _.r(PrivateAccError(self.username))
        except KeyError:
            _.p("There might be an issue with json response in stegram:_verifyPrivAccAccess, please report it to the issue section. This issue isn't fatal.")
        else:
            pass
    
    def _followListScraper(self,h:str,has_next_page=True,act_attempts=0,att=3) -> list:
        """Scrapes the follow list (precised with the hash) of the target username
        Only "h" matters: hash"""
        targlist = _targListToHashesAndViceV(h)
        total_follow = self.acc_infos[targlist]

        pbar = tqdm(total=total_follow, desc=f"""{LOGOS["Python"] if _.colors else _no_colors(LOGOS["Python"])} {targlist.capitalize()} extraction""")
        follow_list = []

        var = {"id":self.target_ig_id,"first":50}
        params = {"query_hash":h,"variables":dumps(var)}

        def resolver(json_resp:dict) -> bool:
            json_resp = json_resp["data"]["user"]["edge_followed_by" if h == "c76146de99bb02f6415203be841dd25a" else "edge_follow"]

            for node in json_resp["edges"]:
                pbar.update(1)
                follow_list.append(node["node"]["username"])

            if json_resp["page_info"]["has_next_page"]:
                var["after"] = json_resp["page_info"]["end_cursor"]
                return True
            return False

        while has_next_page and act_attempts < att:
            queryAPIResp = requests.get("https://www.instagram.com/graphql/query/", params=params, cookies=self.cookies)
            if not queryAPIResp.cookies.get_dict():
                _.r(PrivateAccError(self.username))
            elif queryAPIResp.status_code == 200:
                act_attempts = 0
                has_next_page = resolver(queryAPIResp.json())
                if has_next_page:
                    params["variables"] = dumps(var)

            else:
                act_attempts += 1
                _.p(f"{act_attempts}/{att} attempts, sleeping 10 sec")
                sleep(10.0)

        pbar.close()
        if has_next_page: # Travail est pas fini, donc qu'il y a eu une couille
            _.r(RateLimitError("Rate limit happenning during list of follows scraping. Wait a bit, or change of login account."))

        return follow_list

    def scrapeTargetLists(self) -> tuple:
        """Returns the list to scrape depending on both or not, and on the data already known to block every error that could happen in the process"""
        follow_counts_list = [self.acc_infos[k] for k in ['followers','following']]
        if 0 in follow_counts_list:
            if follow_counts_list == [0,0]:
                _.r(NoFollowError())
            empty_usernames_list_name = [k for k in ['followers','following'] if self.acc_infos[k] == 0][0]

            if self.target_list == "mutuals":
                _.r(MutualsError("No mutuals possible since followers or following list is empty."))
            elif self.target_list == "both":
                _.r(NoFollowError(f"""\"Both" list can't be retrieved since your target has no {empty_usernames_list_name}."""))
        
            elif self.target_list == empty_usernames_list_name:
                _.r(NoFollowError(f"{self.target_list.capitalize()} can't be scraped since it is empty"))
            
        scraping_hashes = _targListToHashesAndViceV(self.target_list)
        follow_usernames = []
        for hash in scraping_hashes:
            follow_usernames.append(self._followListScraper(hash))

        return tuple(follow_usernames)

    def distractAPI(self) -> None: # Not used for now
        """Function made to call a random instagram API other than /USERNAME/?__a/1 to "simulate" very badly an human doing something else.
        These endpoints are sensitive;
        - some of the responses contains personnal informations such as login places, phone numbers, email adresses, ...
        - some of the endpoints can also change your account parameters.
        
        NO DATA IS SAVED, WE ONLY GET THE STATUS CODE OF THE RESPONSE
        NO DATA IS POSTED, ALL REQUESTS ARE get REQUESTS"""
        endpoints = ENDPOINTS_TEST_LIST
        requests.get(f"""https://www.instagram.com/{choice(endpoints)}""", headers=self.default_h, cookies=self.cookies).close()
    
    def getUsernameDetails(self,l:list,already:list=None) -> list:
        """Returns list of ?__a=1 details on each accounts
        -l:list of account, -already:part already exported"""
        self.express = self._canExpress(len(l)) if self.express is None else self.express
        # Vu que la liste de mutuels est calculée après le __init__, on actualise le self.express en fonction de la longueur de la liste.

        done = already if already else []
        lWithoutDone = [x for x in l if x not in [y["username"] for y in already]] if already else l

        if not self.express and len(l) > 20:
            _.p(f"""Exportation in normal mode can take a while. It is normal. {str(underline("You are free to do something else during this time"))}.""", logo="i")

        pbar = tqdm(total=len(l), desc=f"""{LOGOS["Instagram"] if _.colors else _no_colors(LOGOS["Instagram"])} Getting users details""")
        pbar.update(len(done))

        def outputDict(d:dict,username:str=None) -> dict:
            """Converts the raw dict to a selected informations dict"""
            ret = {}
            isNotFound = False
            try:
                d = d['graphql']['user']
                d["link"] = f'''https://www.instagram.com/{d["username"]}/'''
            except KeyError:
                isNotFound = True


            if isNotFound:
                classicKeys = ["id","username","full_name","link","biography","is_private","followers","following","posts","external_url","is_business_account","is_professional_account","is_verified"]
                allInfoKeys = ['business_address_json','business_category_name','business_contact_method','business_email','business_phone_number','connected_fb_page','edge_mutual_followed_by','count','has_ar_effects','has_channel','has_clips','has_guides','hide_like_and_view_counts','is_joined_recently']
                for elemPath in (classicKeys+allInfoKeys if self.all_infos else classicKeys):
                    ret[elemPath] = username if elemPath == "username" else None

            else:
                # Paths à aller chercher dans le Json brut
                classicKeys = [['id'],['username'],['full_name'],['link'],['biography'],['is_private'],['edge_followed_by','count'],['edge_follow','count'],['edge_owner_to_timeline_media','count'],['external_url'],['is_business_account'],['is_professional_account'],['is_verified']]
                allInfoKeys = [['business_address_json'],['business_category_name'],['business_contact_method'],['business_email'],['business_phone_number'],['connected_fb_page'],['edge_mutual_followed_by','count'],['has_ar_effects'],['has_channel'],['has_clips'],['has_guides'],['hide_like_and_view_counts'],['is_joined_recently']]

                # Changement du nom de la nouvelle clée si ancienne première clée du path présent dans ce dict:
                custom_Keys = {'edge_followed_by':'followers','edge_follow':'following','edge_owner_to_timeline_media':'posts','edge_mutual_followed_by':'mutual_followed_by_count'}

                for elemPath in (classicKeys+allInfoKeys if self.all_infos else classicKeys): # Pour élément dans liste de path par défaut (+all_infos si self.all_infos)
                    c = custom_Keys[elemPath[0]] if elemPath[0] in list(custom_Keys.keys()) else False # Changement de clé = False si pas dans le dict de remplacement de clées
                    j = d
                    for key in elemPath:
                        j = j[key]
                        if key == elemPath[-1]: # Lorsque l'on arrive au bout du path, on enregistre dans le dict à sortir
                            ret[c if c else key] = j
            
            return ret

        def normalExtract(ret:list) -> list:
            """Calls to ?__a=1 for each username in normal speed"""
            with requests.Session() as s:
                for i, u in enumerate(lWithoutDone):
                    rep = s.get(f'https://www.instagram.com/{u}/channel/?__a=1',headers={'User-Agent':USER_AGENT,'Referer':f'https://www.instagram.com/{u}'},cookies=self.cookies,allow_redirects=False)
                    sleep(self.delay)
                    if rep.status_code == 200:
                        ret.append(outputDict(loads(rep.text)))
                        pbar.update(1)

                    elif rep.status_code == 404:
                        ret.append(outputDict({},u))
                        
                    # if i > 3: break # volontary rate limit for tests

            return ret

        async def expressExtract(ret:list) -> list:
            """Calls to ?__a=1 for each username in asynchronous speed"""
            async with ClientSession() as s:
                async def fetch(u:str):
                    """Process the request and append the result"""
                    async with s.get(f'https://www.instagram.com/{u}/channel/?__a=1',headers={'User-Agent':USER_AGENT,'Referer': f'https://www.instagram.com/'},cookies=self.cookies,allow_redirects=False) as __a1:
                        if __a1.status == 200:
                            ret.append(outputDict(await __a1.json()))
                            pbar.update(1)
                        
                        elif __a1.status == 404:
                            ret.append(outputDict({},u))

                rq_corro = []
                for u in lWithoutDone:
                    rq_corro.append(fetch(u))
                futures = gather(*rq_corro)
                await futures
                await s.close()
            
            return ret

        rtr = get_event_loop().run_until_complete(expressExtract(done)) if self.express else normalExtract(done)
        pbar.close()
        return rtr