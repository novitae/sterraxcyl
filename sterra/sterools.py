from os import path, makedirs
from sterra._sterrage_ import PATH_TO_CHECK, HISTORY_PATH, CLEARED_HISTORY

# USERNAME LISTS ----------------------------------------------
def makeMutuals(t:tuple) -> list: #
    """Returns username in both lists contained in the input tuple"""
    l1, l2 = t
    _max = l1 if len(l1) >= len(l2) else l2
    _min = l1 if _max == l2 else l2
    return [u for u in _min if u in _max]

# PATH / NAMES ------------------------------------------------
def checkPaths() -> list: #
    rtr = []
    for p in PATH_TO_CHECK:
        if not path.exists(p):
            makedirs(p)
            rtr.append(f"Path {p} created.")
    
    try:
        open(HISTORY_PATH,"r").close()
    except FileNotFoundError:
        rtr.append(f"Path {HISTORY_PATH} created.")
        open(HISTORY_PATH,"w").write(CLEARED_HISTORY)

    return rtr

def isId(p:str) -> bool: #
    """Returns True if id, False if path"""
    try:
        int(p)
        return True
    except ValueError:
        return False