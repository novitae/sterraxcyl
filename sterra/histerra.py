from sterra._sterrage_ import HISTORY_PATH,CLEARED_HISTORY,PARTS_PATH
from json import loads, dumps
from time import time
from re import findall
from os import remove
from stringcolor import *

ACTUAL_HISTORY:dict = loads(open(HISTORY_PATH,"r").read())
PDICT = ACTUAL_HISTORY["part"]

def _mkId() -> str:
    return str(time()).replace(".","")

def all(**kwargs) -> dict:
    """Returns all the history under dict"""
    return ACTUAL_HISTORY

def clear(**kwargs) -> str:
    """Returns True when the history has been cleared"""
    if input("You are about to clear your export history. Y to confirm, other to abort.\n -> ").lower() == "y":
        with open(HISTORY_PATH,"w") as w:
            w.write(CLEARED_HISTORY)
        return "Export history cleared."
    return "Export history cleaning failed."

def file_id(fileid:str=None,**kwargs) -> str:
    """Returns the path associated to an id"""
    Id = fileid if fileid else kwargs.get("file_id")
    if Id:
        for k, v in ACTUAL_HISTORY.items():
            if k == Id:
                return f"""Path associated to id {Id}:\n    {v["path"]}""" if kwargs.get("tostr") else v["path"]
    return f"Path associated to id {Id} found." if kwargs.get("tostr") else None

def match(**kwargs) -> dict:
    """Returns elements of history matching with input"""
    Match = kwargs.get("match")
    isRegex = Match[1:-1] if "??" == Match[0]+Match[-1] else False
    matching = {}
    for k, v in ACTUAL_HISTORY.items():
        if k == "part":
            pass
        else:
            if isRegex and findall(f"(?:{isRegex})", v["path"]):
                matching[k] = v["path"]
            elif Match in v["path"]:
                matching[k] = v["path"]
    return (f"""Paths matching with {f'regex r"{isRegex}"' if isRegex else Match}:\n    """+"\n    ".join(matching) if matching else ("Nothing found.", "Exception")) if kwargs.get("tostr") else matching

def path(**kwargs) -> str:
    """Returns the id associated to a path"""
    Path = kwargs.get("path")
    for k, v in ACTUAL_HISTORY.items():
        if k != "part":
            if v["path"] == Path:
                return f"Id for path {Path}:\n    {k}" if kwargs.get("tostr") else k
    return f"No id associated to the path {Path} found.", "Exception" if kwargs.get("tostr") else None

def add(**kwargs) -> str:
    """Write down the input dict and returns the id of the stored data"""
    Id = _mkId()
    ACTUAL_HISTORY[Id] = kwargs
    with open(HISTORY_PATH,"w") as w:
        w.write(dumps(ACTUAL_HISTORY,indent=4))
    return Id

def add_part(part_path:str=None, target:str=None) -> str:
    """Return the id of the part created or existing"""
    if part_path:
        return findall(r"[0-9]{16}",part_path)[-1]
    else:
        Id = _mkId()
        Path = f"{PARTS_PATH}{Id}.json"
        PDICT[Id] = {"path":Path,"target":target}
        with open(HISTORY_PATH,"w") as w:
            w.write(dumps(ACTUAL_HISTORY,indent=4))
        return Id, Path

def get_part(part_option:str=True) -> tuple:
    if part_option is True:
        pKeys = list(PDICT.keys())
        return (pKeys[-1], PDICT[pKeys[-1]]["path"], PDICT[pKeys[-1]]["target"])
    try:
        return (part_option, PDICT[part_option]["path"], PDICT[part_option]["target"])
    except KeyError:
        if type(part_option) is str:
            Id = part_option.split("/")[-1].split(".")[0]
            return (Id, PDICT[Id]["path"], PDICT[Id]["target"])
    return None

def clear_parts(**kwargs) -> bool:
    if input("You are about to delete all your parts. Y to confirm, other to abort.\n -> ").lower() == "y":
        try:
            try:
                remove(PARTS_PATH)
            except PermissionError:
                return "Parts deletion failed, os.remove() raised a PermissionError.", "Exception"
            return "Parts deletion done."
        except FileNotFoundError:
            pass
    return "Parts deletion failed.", "Exception"

def compare_tree(**kwargs):
    def climb_the_tree(fileid) -> dict:
        file_path = file_id(**{"file_id":fileid})
        decomposed = exman()._decompose_path(file_path)
        if list(decomposed.keys()) != ["file_path","format","target"]:
            return {"base":decomposed["file_path"]}
        else:
            dcomp_split = decomposed["target"].replace("(","").replace(")","").split("&&" if "&&" in decomposed["target"] else "||")
            return {file_id(**{"file_id":item}):climb_the_tree(item) for item in dcomp_split}
                
    from sterra.exterra import exman
    return f"""History tree for compared file {kwargs["compare_tree"]}:\n"""+dumps({file_id(**{"file_id":kwargs["compare_tree"]}):climb_the_tree(kwargs["compare_tree"])}, indent=4)

