from stringcolor import *
from sterra._sterrage_ import VERSION
from random import choice

HORIZONTAL = "LightSlateBlue" #8787ff
VERTICAL = "Purple" #800080
OTHER = "DarkCyan" #00af87

def _generate_logo() -> str:
    # https://patorjk.com/software/taag/#p=display&h=2&f=Small%20Slant&t=sterra
    GIT_COM = "https://github.com/"
    NAME = "novitae"
    NOVI_URL = f"{GIT_COM}{NAME}"
    VERSION_POSITON = 20

    _LOGO = """           __
      ___ / /_ ___ ________ __ _
     (_-</ __// -_) __/ __/ _ `/
    /___)⎜__/ \__/_/ /_/  \_,_/
    https://github.com/novitae
    ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺ ⎺⎺⎺⎺⎺⎺ ⎺⎺ ⎺"""
    _LOGO = _LOGO[:VERSION_POSITON]+cs(VERSION,OTHER).underline().bold()+_LOGO[VERSION_POSITON+len(VERSION):]

    for char in "(/|,)⎜\\<`_-⎺":
        _LOGO = _LOGO.replace(char,str(cs(char, HORIZONTAL if char in "_-⎺" else VERTICAL).bold()))
    return _LOGO.replace(NOVI_URL.replace("/", str(cs("/",VERTICAL).bold())), str(cs(NOVI_URL,OTHER).underline()))

def _return_infos() -> str:
    def random_col(s) -> str:
        return "".join([str(cs(l,choice([HORIZONTAL,"SteelBlue3","SteelBlue4","SlateBlue4"]))) for l in s])
    L = []
    messages = str(f"""
     {cs("A SOCMINT tool for Instagram using follow lists;",OTHER).underline()}
    * {random_col("Export followers / following / mutuals of your target")}
    * {random_col("Compare lists to find mutuals, non-mutuals and evolutions")}
    * {random_col("Lists analysis to get close circle accounts probabilites")}""").split("\n")
    for i, line in enumerate(_generate_logo().split("\n")):
        try:
            L.append(line+messages[i].replace("*",str(cs("*",OTHER))))
        except IndexError:
            L.append(line)

    return "\n".join(L)

LOGO = _generate_logo()