from sterra.histerra import file_id, add_part, add, get_part, match
from sterra._sterrage_ import DEFAULT_EXPORT_PATH, DAY_STRF, HOUR_STRF
from datetime import date, datetime
from os.path import join, exists
from re import findall

REFDIC = dict(
    us="username",
    ta="target",
    da="date",
    ho="hour",
    li="list_id"
)

class exman:
    """exman is manage exports, rule names, type of export, etc ...
    The export was causing too much exceptions about names and shit, it wasn't possible to continue like this"""
    def __init__(self, _:object=None) -> None:
        self._ = _

    def _decompose_path(self, file_path:str) -> dict:
        """Decompose the path to get all the informations on the file"""
        retour = {
            "file_path": file_path
        }
        filenm = file_path.split("/")[-1] if "/" in file_path else file_path
        fsplit = filenm.split(".")
        retour["name"] = fsplit[0]
        retour["format"] = fsplit[-1]
        try:
            if "&&" in fsplit[0]:
                fsplit[0].replace("&&","@@")
            for k, v in [tuple(item.split(";")) for item in fsplit[0].split("&")]:
                retour[REFDIC[k]] = v.replace("@@","&&")
        
        except ValueError: # For names like "ta;(16441852344045281&&1644185302525507).csv" that doesn't have "&"
            if findall(r"[0-9]{8,20}\.", filenm) and not ";" in fsplit[0]: # For parts
                pass
            else:
                try:
                    k, v = fsplit[0].split(";")
                    retour[REFDIC[k]] = v
                except ValueError: # Custom names (e.g.: bleu.xlsx)
                    pass

        return retour

    def _make_pathfiles(self, path:str, name:str) -> str:
        """Makes the dirs if the pathfile doesn't exist"""
        def buildPath(path, name):
            newpath = join(path, name)
            try:
                open(newpath,"r").close()
                raise FileExistsError
            except FileNotFoundError:
                return newpath

        ext = name.split(".")[-1]
        newpath = None
        while not newpath:
            try:
                newpath = buildPath(path=path, name=name)
            except FileExistsError:
                self._.p(f"File name \"{name}\" already exists. Choose a new one:", logo="Interrogation")
                name = f"""{input("    -> ")}.{ext}"""

        if not exists(newpath):
            from os import makedirs
            try:
                makedirs("/".join(newpath.split("/")[:-1])+"/")
            except FileExistsError:
                pass
        Id = add(**dict(path=newpath))
        return Id, newpath

    def part(self, target_list:str, part_path:str=None) -> str:
        if part_path:
            exists = get_part(part_path)
            if type(exists) is tuple:
                return exists
            else:
                return add_part(target=target_list)
        else:
            return add_part(target=target_list)

    def custom_name(self, name:str, Format:str="xlsx", path:str=DEFAULT_EXPORT_PATH) -> str:
        """"""
        return self._make_pathfiles(path, f"{name}.{Format}")

    def classic_export(self, target:str, username:str, Format:str="xlsx", path:str=DEFAULT_EXPORT_PATH) -> str:
        """"""
        return self._make_pathfiles(path, f"""us;{username}&ta;{target}&da;{date.today().strftime(DAY_STRF)}&ho;{datetime.now().strftime(HOUR_STRF)}.{Format}""")

    def compare_export(self, file1:str, file2:str, target:str, Format:str="xlsx", path:str=DEFAULT_EXPORT_PATH) -> str:
        """"""
        file_ids = [list(match(**{"match":f}).keys())[0] for f in [file1, file2]]
        if None in file_ids:
            raise Exception("Couille ici")
        return self._make_pathfiles(path, f"""ta;({("&&" if target == "common_usernames" else "||").join(file_ids)}).{Format}""")
        
    def analysis_export(self, list_id:str, target:str, Format:str="xlsx", path:str=DEFAULT_EXPORT_PATH) -> str:
        """"""
        return self._make_pathfiles(path, f"""li;{list_id}&ta;{target}.{Format}""")
        # li == list_id

#+ ajouter ddate et heure a tous les noms ???