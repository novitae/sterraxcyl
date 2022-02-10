from sterra.sterools import makeMutuals, isId, checkPaths
from sterra._logo_ import LOGO
from sterra._outputs_ import _ as outputs
from sterra._sterrage_ import DEFAULT_EXPORT_PATH, HISTORY_ARG_KEYS, PROG, DESCRIPTION, EPILOG, HISTORY_ARGUMENTS, HISTORY_STORE_TRUE, HISTORY_PATH, PARTS_PATH
from sterra.SterraException import RateLimitError, BadListOfDictError, ExportDataError, EmptyResultError

from argparse import ArgumentParser, SUPPRESS
from stringcolor import *

from sterra.filerra import *
from sterra.stegram import _instagram
from sterra.comparerra import _compare
from sterra.stanalysis import _analysis
from sterra.exterra import exman
import sterra.histerra as hst
import sys
import json

#+ -> to do
#! -> vulnerable point

global _
_ = outputs()

def EXPORT(**kwargs) -> bool:
    """Exports the follow list targeted and the information of the accounts in it"""
    def autoLaunchBack(flist:list) -> list: # Not used for now
        """Relaunch the process everytime it gets blocked until the work is done"""
        lback_scraped = already if already else []
        while len(lback_scraped) != len(flist):
            lback_scraped = scraper.getUsernameDetails(flist, already=lback_scraped)
            scraper.distractAPI()
        return lback_scraped

    def scrape(targlist:str,flist:list) -> None:
        """Scrapes the data of usernames in flist and returns the id of the file in wich it has been written"""
        if kwargs.get("only_usernames"):
            _.p(f"""{username}'s {targlist} usernames file exported under id: {str(bold(exporter([{"username":usn} for usn in flist],_,**kwargs)()))}""",logo=logo_to_choose)

        else:
            # if kwargs.get("auto_launckback"):
            #     __a1List = autoLaunchBack(flist)
            # else:
                __a1List = scraper.getUsernameDetails(flist, already=already)
                
                if len(__a1List) != len(flist): # Export en part
                    values = exman(_).part(targlist, part_path)
                    try:
                        pid, file_path, _t = values
                    except ValueError:
                        pid, file_path = values
                    exporter(_, __a1List, file_path, Format="json")()
                    _.r(RateLimitError(f"Part file exported under id: {str(bold(pid))}"))
                
                else: # Export classique
                    fid, file_path = exman(_).custom_name(name=kwargs["name"], Format=kwargs["format"], path=kwargs["path"]) if kwargs.get("name") else exman(_).classic_export(target=targlist, username=username, Format=kwargs["format"], path=kwargs["path"])
                    exporter(_=_, List=__a1List, file_path=file_path, Format=Format, **{"username":username,"target":targlist})()
                    _.p(f"""{username}'s {targlist} list exported under id: {str(bold(fid))}""",logo=logo_to_choose)
    
    # Options de parts
    part_option = kwargs.get("part")
    part_path = None

    if part_option:
        _i, part_path, target_list = hst.get_part(part_option)
        kwargs["target"] = target_list
        _.p("Reading part content ...",logo="json")
        part_content = reader(_, part_path)()
    else:
        target_list = kwargs["target"]

    already = part_content if part_option else None
    original_target = kwargs["target"]
    logo_to_choose = Format = kwargs["format"]
    scraper = _instagram(_, original_target, **kwargs)
    
    lists = scraper.scrapeTargetLists()
    kwargs["username"] = username = scraper.username

    follow_list = (
        {target_list:lists[0]} if target_list in ["followers","following"]
        else {"followers":lists[0],"following":lists[1]} if target_list == "both"
        else {"mutuals":makeMutuals(lists)}
        )

    for t, l in follow_list.items():
        scrape(t,l)

    return True

def COMPARE(**kwargs):
    """Compare lists between them to return commons or differences"""
    Format = logo_to_choose = kwargs.get("format")
    no_print = kwargs.get("no_print")
    fi = kwargs.get("fi")

    ordre = (1, 0) if kwargs.get("invert") else (0, 1)
    f1p, f2p = fi[ordre[0]], fi[ordre[1]]
    l1, l2 = reader(_=_, file_path=f1p)(), reader(_=_, file_path=f2p)()

    c = _compare(_, l1, l2)
    if not no_print:
        _.p(f"""Between {underline(f1p.split("/")[-1])} and {underline(f2p.split("/")[-1])},""",logo="Compare")
    for targ_comp in ["common_usernames","not_common_usernames"]:
        if kwargs.get(targ_comp):
            r = getattr(c,targ_comp)()
            if not r:
                _.r(EmptyResultError())

            if not no_print:
                _.p(f"""    {bold(targ_comp.capitalize().replace("_"," "))}:""")
                for item in r:
                    _.p("    -> "+(underline("".join([str(cs(item, color)) for item, color in {"https://www.instagram.com/":'LightGrey13',item["username"]:'LightGrey5',"/":'LightGrey13'}.items()])) if kwargs.get("url") else item["username"]))

            if kwargs.get("export"):
                if r:
                    fid, file_path = exman(_).custom_name(name=kwargs["name"], Format=Format, path=kwargs["path"]) if kwargs.get("name") else exman(_).compare_export(file1=f1p, file2=f2p, target=targ_comp, Format=Format, path=kwargs["path"])
                    exporter(_=_, List=r, file_path=file_path, Format=Format, **{"target":targ_comp})()
                    _.p(f"""Comparaison exported under id: {str(bold(fid))}""",logo=logo_to_choose)
                else:
                    _.r(ExportDataError("the compared result is empty"))
    return True

def ANALYSE(**kwargs) -> bool:
    def arrow_color(i:float) -> str:
        colors = ['Black','DarkRed','DarkRed2','Red4','Red3','Red2','Red','OrangeRed','DarkOrange','Orange','LightGoldenrod2','Yellow','Yellow2','Yellow3','Yellow4','GreenYellow','Chartreuse2','Green2','Green3','Green4']
        return str(cs("->",colors[int(i/5)]))

    Format = logo_to_choose = kwargs.get("format")
    path = kwargs["fi"]
    data = reader(_=_, file_path=path)()
    
    required_keys = ['biography',"full_name",'is_private','followers','following','external_url','is_verified','posts','is_professional_account','is_business_account',"id"]
    missing_keys = [k for k in required_keys if k not in list(data[0].keys())]
    if missing_keys:
        _.r(BadListOfDictError(missing_keys[0]))    

    for analyse_targ in ["personnal","interests"]:
        if kwargs.get(analyse_targ):
            analysed = _analysis(_=_, data=data, **kwargs)(analyse_targ)
            # example # analysed = [{"username":"username","%":x*5} for x in range(20)]
            if not kwargs.get("no_print"):
                _.p(f"""Probabilites for {bold(analyse_targ.replace("_"," "))} accounts in {underline(path.split("/")[-1])}:\n    %% -> username""", logo="Analyse")
                for account in analysed:
                    _.p(f"""    {str(
                        str(int(account["%"])))+" " if account["%"] < 10 else str(int(account["%"]))} {arrow_color(account["%"])} {"".join([str(cs(item, color)) for item, color in {"https://www.instagram.com/":'LightGrey13',account["username"]:'LightGrey5',"/":'LightGrey13'}.items()]
                        ) if kwargs.get("url") else account["username"]}""")

            if not analysed:
                _.r(EmptyResultError())

            if kwargs.get("export"):
                list_id = hst.path(**{"path":path})
                fid, file_path = exman(_).custom_name(name=kwargs["name"], Format=Format, path=kwargs["path"]) if kwargs.get("name") else exman(_).analysis_export(list_id=list_id, target=analyse_targ, Format=Format, path=kwargs["path"])
                exporter(_=_, List=analysed, file_path=file_path, Format=Format, **kwargs)()
                _.p(f"""Analyse exported under id: {str(bold(fid))}""",logo=logo_to_choose)

    return True

def CONVERT(**kwargs) -> bool:
    infoList = reader(_, kwargs["fi"])()
    infos =  exman(_)._decompose_path(kwargs["fi"])
    name = kwargs["name"] if kwargs.get("name") else infos["name"]
    fid, file_path = exman(_).custom_name(name=name, Format=kwargs["format"], path=kwargs["path"])
    exporter(_=_, List=infoList, file_path=file_path, Format=kwargs["format"])()
    _.p(f"""Converted file exported under id: {str(bold(fid))}""", logo=kwargs["format"])
    return True

def HISTORY(**kwargs:dict) -> None:
    funcKey = list(kwargs.keys())[0]
    kwargs["tostr"] = True
    respnse = getattr(hst,funcKey)(**kwargs)
    if type(respnse) is tuple:
        rep, logo = respnse
        _.p(rep, logo=logo)
    else:
        if type(respnse) is dict:
            toPr = ("\n    ".join([f"""{k} -> {json.dumps(v) if k == "part" else v["path"]}""" for k, v in respnse.items()]))
            if funcKey == "all":
                _.p(f"Full history:\n    {toPr}", logo="i")
        else:
            _.p(respnse, logo="i")
    return None

def _parser() -> tuple[str, dict]:
    ARG_FORMAT = "format of the file (default:\"excel\")"
    ARG_EXPORT_PATH = f"""path to the directory to export the file(s) (default:"{DEFAULT_EXPORT_PATH}")"""
    ARG_SELECTED_FILE = "id or path of the file"
    ARG_URL = "print url instead of usernames"

    def _formatDefault(a:dict) -> dict:
        """Capture les erreurs d'arguments, change les id de path en path."""
        _.colors = False if a.get("no_colors") else True
        _._raise = a.get("raw_raising")

        wich = a["wich"]
        no_false = {k:v for k,v in a.items() if (k if wich == "analyse" else v)} # Analyse module needs all value including None or False
        nfKeys = list(no_false.keys())

        if wich in ["compare","analyse"]:
            if wich == "compare":
                compare_requ_args = ["not_common_usernames","common_usernames"]
                if not set(compare_requ_args) & set(list(no_false.keys())):
                    parser.error(f"""compare: compare requires at least one of the arguments: {", ".join([f'''--{x.replace("_","-")}''' for x in compare_requ_args])}""")

            elif wich == "analyse":
                analyse_requ_args = ["personnal","interests"]
                if not [item for item in list(no_false.keys()) if a[item] and item in analyse_requ_args]:
                    no_false["personnal"] = True

            if wich in ["compare","analyse"]:
                if a["no_print"] and not a["export"]:
                    parser.error(f"{wich}: {wich} requires --export if you choose --no-print (avoids making a job without any output)")

        if wich == "history":
            if len([k for k, v in no_false.items() if k in HISTORY_ARG_KEYS]) != 1:
                parser.error("history: history module requires only one argument between the ones available")
        
        if no_false.get("no_exp_limit") and not a.get("express"):
            parser.error("export: --no-exp-limit can't be applied if --express is not enabled")
        
        if "fi" in nfKeys:
            if type(no_false["fi"]) is list:
                no_false["fi"] = [(hst.file_id(fi) if isId(fi) else fi) for fi in no_false["fi"]]
                if None in no_false["fi"]:
                    _.r(IndexError('One of the input fileId have not been found in the history.'))
            else:
                no_false["fi"] = hst.file_id(no_false["fi"]) if isId(no_false["fi"]) else no_false["fi"]
                if not no_false["fi"]:
                    _.r(IndexError('The input fileId have not been found in the history.'))
        
        if "format" in nfKeys:
            no_false["format"] = no_false["format"] if no_false["format"] != "excel" else "xlsx"

        if "name" in nfKeys:
            classic_err = "--name can't be used to export two files (they would have the same name)"
            if wich == "export":
                if no_false.get("target") == "both":
                    parser.error(classic_err)
            
            elif wich == "compare":
                if "not_common_usernames" in nfKeys and "common_usernames" in nfKeys and "export" in nfKeys:
                    parser.error(classic_err)

            elif wich == "analyse":
                if a["personnal"] and a["interests"] and a["export"]:
                    parser.error(classic_err)

        no_false.pop("wich")
        return no_false

    parser = ArgumentParser(prog=PROG,description=DESCRIPTION,epilog=EPILOG)
    
    parser.add_argument("--raw-raising", action="store_true",
                        help="raises Exceptions with python \"raise\"; useful for debug.")
    parser.add_argument("--no-colors", action="store_true",
                        help="print all outputs in b&w")

    sub_parsers = parser.add_subparsers()

    # export
    export_parser = sub_parsers.add_parser("export", add_help=False, epilog="https://github.com/novitae/sterraxcyl/wiki/Export")
    
    exp_required = export_parser.add_argument_group(title="positional arguments")
    exp_exclued_username = exp_required.add_mutually_exclusive_group(required=True)
    exp_exclued_username.add_argument("-u", "--username", metavar="U", type=str,
                        help="target's instagram username")
    exp_exclued_username.add_argument("-id", metavar="ID", type=int,
                        help="target's instagram id")
    exp_exclued_target = exp_required.add_mutually_exclusive_group(required=True)
    exp_exclued_target.add_argument("-t", "--target", choices=["followers", "following", "both", "mutuals"],
                        help="list to export")
    exp_exclued_target.add_argument("-p", "--part", const=True, nargs="?",
                        help="id of the part") # The part id leads to a dict in history containing its path and the target list
    
    exp_login = export_parser.add_argument_group(title="login arguments")
    exp_exc_login = exp_login.add_mutually_exclusive_group(required=True)
    exp_exc_login.add_argument("-lcrd", "--login-credentials", metavar=("U", "P"), nargs=2,
                        help="login by credentials (USERNAME PASSWORD)")
    exp_exc_login.add_argument("-ssid", "--login-session-id", metavar="S",
                        help="login by sessionid")

    exp_export = export_parser.add_argument_group(title="export arguments")
    exp_export_data = exp_export.add_mutually_exclusive_group()
    exp_export_data.add_argument("--all-infos", action="store_true",
                        help="exports extra informations (not interesting ones)")
    exp_export_data.add_argument("--only-usernames", action="store_true",
                        help="exports only the usernames, not the data linked to")
    exp_export.add_argument("-f", "--format", choices=["excel", "csv", "json"], default="excel",
                        help=ARG_FORMAT)
    exp_export.add_argument("--path", metavar="P", default=DEFAULT_EXPORT_PATH,
                        help=ARG_EXPORT_PATH)
    exp_export.add_argument("--name", metavar="N",
                        help="custom name for the exported file")

    exp_speed = export_parser.add_argument_group(title="speed arguments")
    exp_exc_speed = exp_speed.add_mutually_exclusive_group()
    exp_exc_speed.add_argument("-d", "--delay", type=int,
                        help="delay between requests")
    exp_exc_speed.add_argument("-e", "--express", action="store_true",
                        help="express requests (deactivated if > 109 total usernames to avoid blocking)")

    exp_optional = export_parser.add_argument_group(title="optional arguments")
    exp_optional.add_argument("--no-exp-limit", action="store_true",
                        help="disable the username count limitation on express mode")
    # For the day instagram will find a way to put a more frequent ratelimit
    #exp_optional.add_argument("--auto-launchback", action="store_true",
    #                    help="relaunch automatically the scraping while all usernames haven't been scraped")
    exp_optional.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='show this help message and exit')
    
    export_parser.set_defaults(wich="export")

    # compare
    compare_parser = sub_parsers.add_parser("compare", epilog="https://github.com/novitae/sterraxcyl/wiki/Compare")

    compare_parser.add_argument("fi", metavar="{ID,PATH} {ID,PATH}", nargs=2,   # Must do a metavar like this to avoid:
                        help=f"{ARG_SELECTED_FILE}s to compare")                # https://stackoverflow.com/questions/20680882/in-python-argparse-crashes-when-using-h
    compare_parser.add_argument("-n", "--no-print", action="store_true",
                        help="doesn\"t print results")
    compare_parser.add_argument("-u", "--url", action="store_true",
                        help=ARG_URL)
    compare_parser.add_argument("-i", "--invert", action="store_true",
                        help="invert the order of the lists")

    com_want = compare_parser.add_argument_group(title="action")
    com_want.add_argument("--common-usernames", action="store_true",
                        help="commons usernames between lists")
    com_want.add_argument("--not-common-usernames", action="store_true",
                        help="not commons usernames between lists (result vary depending on the list order; use --invert)")

    comp_export = compare_parser.add_argument_group(title="export data")
    comp_export.add_argument("-e", "--export", action="store_true",
                        help="export the result")
    comp_export.add_argument("-f", "--format", choices=["excel", "csv", "json"], default="excel",
                        help=ARG_FORMAT)
    comp_export.add_argument("-p", "--path", default=DEFAULT_EXPORT_PATH,
                        help=ARG_EXPORT_PATH)
    comp_export.add_argument("--name", metavar="N",
                        help="custom name for the exported file")

    compare_parser.set_defaults(wich="compare")

    # analyse
    analyse_parser = sub_parsers.add_parser("analyse", epilog="https://github.com/novitae/sterraxcyl/wiki/Analyse")

    analyse_parser.add_argument("fi", metavar="{ID,PATH}",
                        help=f"{ARG_SELECTED_FILE} to analyse")
    analyse_parser.add_argument("-i", "--invert", action="store_true",
                        help="print by the end of the list")
    analyse_parser.add_argument("-e", "--export", action="store_true",
                        help="export results")
    analyse_parser.add_argument("-f", "--format", choices=["excel", "csv", "json"], default="excel",
                        help=ARG_FORMAT)
    analyse_parser.add_argument("--ignore-over", type=int,
                        help="quantity of followers over wich we consider the account as impossible to be in the close circle of the target (default:10000)")
    analyse_parser.add_argument("--name", metavar="N",
                        help="custom name for the exported file")
    analyse_parser.add_argument("--no-print", action="store_true",
                        help="don't print results")
    analyse_parser.add_argument("-p", "--path", default=DEFAULT_EXPORT_PATH,
                        help=ARG_EXPORT_PATH)
    analyse_parser.add_argument("--pctg", type=int,
                        help="percentage under wich results will not be printed (between 0 and 98)")
    analyse_parser.add_argument("-s", "--size", type=int,
                        help="size of the output")
    analyse_parser.add_argument("-u", "--url", action="store_true",
                        help=ARG_URL)

    ana_want = analyse_parser.add_argument_group(title="analysis")
    ana_want.add_argument("--personnal", action="store_true",
                        help="probabilities for close circle accounts")
    ana_want.add_argument("--interests", action="store_true",
                        help="probabilities for interests account")

    analyse_parser.set_defaults(wich="analyse")

    # convert
    convert_parser = sub_parsers.add_parser("convert", epilog="https://github.com/novitae/sterraxcyl/wiki/Convert")
    
    convert_parser.add_argument('fi', metavar="{ID,PATH}",
                        help=f'{ARG_SELECTED_FILE} to convert')
    convert_parser.add_argument('-f', '--format', choices=['excel', 'csv', 'json'], required=True,
                        help=ARG_FORMAT)
    convert_parser.add_argument("--name", metavar="N",
                        help="custom name for the exported file")
    convert_parser.add_argument("-p", "--path", metavar="P", default=DEFAULT_EXPORT_PATH,
                        help=ARG_EXPORT_PATH)

    convert_parser.set_defaults(wich="convert")

    # history
    history_parser = sub_parsers.add_parser("history", usage=f"""sterra history [-h] {{{"|".join([(f"--{a}" if a in HISTORY_STORE_TRUE else f"--{a} {a.upper()}") for a in HISTORY_ARGUMENTS])}}}""", epilog="https://github.com/novitae/sterraxcyl/wiki/History")
    
    history_parser.add_argument("-a", f"--all", action="store_true",
                        help=f"""show all the export history""")
    history_parser.add_argument(f"--clear", action="store_true",
                        help=f"""clear the history""")
    history_parser.add_argument(f"--clear-parts", action="store_true",
                        help=f"""delete all part stored""")
    history_parser.add_argument(f"--compare-tree",
                        help=f"""shows the tree of a compare file""")
    history_parser.add_argument("-i", f"--file-id",
                        help=f"""show the path associated to the filled id""")
    history_parser.add_argument("-m", f"--match",
                        help=f"""show the items containing the filled string (can be a regex if it is used like ' ?"YOUR REGEX"? ')""")
    history_parser.add_argument("-p", f"--path",
                        help=f"""show the id associated to the filled path""")
    
    history_parser.set_defaults(wich="history")

    args = parser.parse_args()
    
    try:
        return args.wich, _formatDefault(vars(args))
    except AttributeError:
        parser.exit(parser.print_help())

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        _.p("To uninstall properly sterra, run the following commands:",logo="Python")
        _.p(f" $ sudo rm -rf {DEFAULT_EXPORT_PATH}")
        _.p(f" $ sudo rm -rf {PARTS_PATH}")
        _.p(f" $ sudo rm -rf {HISTORY_PATH}")
        _.p(f" $ pip uninstall sterra")
    
    else:
        module, kwargs = _parser()
        _.p(LOGO)
        ret = globals()[module.upper()](**kwargs)
        if ret:
            _.p("If you have ideas to improve this program, don't hesitate to write them in the issue section !",logo="Plus")

if __name__ == "__main__":
    main()
