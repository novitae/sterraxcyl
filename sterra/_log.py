import requests
import time
import re
import random

from datetime import datetime
from sterra import _pri
from sterra import _user
'''Probablement utilisé de manière plus fréquente lors de prochaines maj en imaginant une liste d'identifiants'''
def in_(u, p):
    '''Returns the sessionid
    - u: username
    - p: password'''
    
    session = requests.Session()
    session.headers.update({
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'www.instagram.com',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/',
        'User-Agent': _user.agent(),
        'X-Instagram-AJAX': '7a3a3e64fa87',
        'X-Requested-With': 'XMLHttpRequest'})

    reponse = session.get('https://www.instagram.com')
    csrf = re.findall(r"csrf_token\":\"(.*?)\"", reponse.text)[0]
    if csrf: session.headers.update({'x-csrftoken': csrf})
    else: _pri.outExcept(e='LoginException: No csrf token found in cookies. Wait 1 hour and retry, or change of account.')
    time.sleep(random.randint(1, 3))

    post_data = {'username': u, 'enc_password': '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), p)}

    response = session.post('https://www.instagram.com/accounts/login/ajax/', data=post_data, allow_redirects=True)
    response_data = response.json()

    if 'two_factor_required' in response_data:
        _pri.outExcept(e='LoginException: Please disable 2-factor authentication to login.')
    if 'message' in response_data and response_data['message'] == 'checkpoint_required':
        _pri.outExcept(e='LoginException: Please check Instagram app for a security confirmation that it is you trying to login.')
    if not response_data['authenticated']:
        _pri.outExcept(e='LoginException: Login failed. Be sure your of your credentials.')

    return response.cookies['sessionid']

def in_sssid(c):
    if type(c) == list: # PAR IDENTIFIANTS
        sssid = in_(c[0], c[1])
    else: # PAR SESSIONID
        if re.match(r'[0-9]{1,32}%[0-9a-zA-Z]{16}%[0-9A-Z]{3,4}', c): sssid = c
        else: _pri.outExcept(e='LoginException: The provided sessionId doesn\'t match normal sessionId format. Verify that you wrote it correctly.\n    If the error is not going away, report it in issue, and write in it this regex "r\'[0-9]{1,32}%[0-9a-zA-Z]{16}%[0-9A-Z]{3,4}\'" with your report.')
    
    return sssid