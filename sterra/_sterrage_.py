from json import dumps
from os import path
from stringcolor import *

# INFOS -------------------------------------------------------
VERSION = "2.2"
PROG = "sterra"
USAGE = ""
DESCRIPTION = "Sterra is a SOCMINT tool to analyse instagram followers|following of a target, and get informations from it."
EPILOG = "WIKI: "+str(underline("https://github.com/novitae/SterraDev/wiki"))

DAY_STRF = "%b-%d-%Y"
HOUR_STRF = "%H-%M-%S"

# PARSER ------------------------------------------------------
HISTORY_STORE_TRUE = ["all","clear","clear-parts"]
HISTORY_ARGUMENTS = {
    "all":"show all the export history",
    "clear":"clear the history",
    "clear-parts":"delete all part stored",
    "compare-tree":"shows the tree of a compare file",
    "file-id":"show the path associated to the filled id",
    "match":"show the items containing the filled string",
    "path":"show the id associated to the filled path"
    }
HISTORY_ARG_KEYS = [x.replace("-","_") for x in list(HISTORY_ARGUMENTS.keys())]
CLEARED_HISTORY = dumps({"part":{}},indent=4)

# USERNAME LISTS ----------------------------------------------
def makeMutuals(t:tuple) -> list:
    """Returns username in both lists contained in the input tuple"""
    l1, l2 = t
    _max = l1 if len(l1) >= len(l2) else l2
    _min = l1 if _max == l2 else l2
    return [u for u in _min if u in _max]

# PATH / NAMES ------------------------------------------------
MODULE_PATH = path.dirname(__file__)

DEFAULT_EXPORT_PATH = path.join(MODULE_PATH,"export/")
PARTS_PATH = path.join(MODULE_PATH,"parts/")
HISTORY_PATH = path.join(MODULE_PATH,'_history_.json')

PATH_TO_CHECK = [DEFAULT_EXPORT_PATH,PARTS_PATH]

# OTHER --------------------------------------------------------
ENDPOINTS_TEST_LIST = [
    'accounts/edit/?__a=1',
    'accounts/manage_access/?__a=1',
    'push/web/settings/?__a=1',
    'session/login_activity/?__a=1',
    'emails/emails_sent/?__a=1',
    'settings/help/?__a=1',
    'accounts/convert_to_professional_account/?__a=1'
    ]