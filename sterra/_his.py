import os
import json
from stringcolor import *
from sterra import _pri

def recreate(PATH):
    with open(PATH, 'w') as a:
        a.write(json.dumps([], indent=4))

DIR = os.path.dirname(__file__)+'/'
PATH = DIR+'EXPORTS-HISTORY.json'
if not os.path.exists(PATH):
    recreate(PATH)

def tory(dd=None, ll=False, nm=None, cl=False):
    '''- dd: Add a str to the historic (experimental),
    - ll: True to print all the historic
    - nm: Prints all path containing the str of nm
    - cl: True to clear the historic'''
    if dd is not None:
        j_add = json.loads(open(PATH, 'r').read())
        j_add.append(dd)
        with open(PATH, 'w') as b:
            b.write(json.dumps(j_add, indent=4))
    
    elif cl:
        validation = input(_pri.Interrrogation()+'Are you sure you want to erase your export historic ? '+bold('There is no coming back after erasing it')+' !\n    ( '+bold('Y')+' | '+bold('N')+' )  --->  ')
        if validation.lower() == 'y':
            recreate(PATH)
            print(_pri.i()+f'Historic erased.')
        else:
            print(_pri.i()+f'Historic not erased.')
    else:
        def output(e):
            print(cs(' >  ', 'DodgerBlue2').bold()+underline(e))
        
        j_ra = json.loads(open(PATH, 'r').read())
        if j_ra == []:
            print(_pri.Exception()+'Empty historic')
        elif ll:
            print(_pri.i()+'Historic of exportation paths:')
            for e in j_ra:
                output(e)
        
        elif nm is not None:
            print(_pri.i()+f'Searching for {nm} in exports historic:')
            notfound = True
            for e in j_ra:
                if nm in e:
                    output(e)
                    if notfound:
                        notfound = False
            if notfound:
                print(_pri.i()+f'Nothing including {nm} found in the historic')