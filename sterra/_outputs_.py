from stringcolor import *
import re

LOGOS = {
    "Analyse": cs('|', 'LightSlateBlue')+bold('%').cs('White', 'LightSlateBlue')+cs('|', 'LightSlateBlue'),
    "Compare": cs('|', 'Salmon')+bold('≈').cs('White', 'Salmon')+cs('|', 'Salmon'),
    "csv": cs('|', 'Orange')+bold('c').cs('White', 'Orange')+cs('|', 'Orange'),
    "xlsx": cs('|', 'Green4')+cs('X', 'White', 'Green4')+cs('|', 'Green4'),
    "Exception": cs('|', 'Red2')+bold('!').cs('White', 'Red2')+cs('|', 'Red2'),
    "i": cs('|', 'DodgerBlue2')+bold('i').cs('White', 'DodgerBlue2')+cs('|', 'DodgerBlue2'),
    "Interrogation": cs('|', 'Violet')+bold('?').cs('White', 'Violet')+cs('|', 'Violet'),
    "Instagram": cs('|', 'LightSalmon2')+cs('o', 'White', 'DeepPink4')+cs('|', 'MediumOrchid'),
    "json": cs('{', 'Purple5').bold()+cs('j', 'DeepSkyBlue4').bold()+cs('}', 'Purple5').bold(),
    "Plus": cs('|', 'DarkSeaGreen9')+bold('+').cs('DarkSeaGreen9', 'White')+cs('|', 'DarkSeaGreen9'),
    "Python": cs('|', 'DeepSkyBlue5')+bold('§').cs('LightGoldenrod2', 'DeepSkyBlue5')+cs('|', 'LightGoldenrod2'),
    "Requests": cs('|', 'SeaGreen2')+bold('$').cs('White', 'DarkGrey')+cs('|', 'LightSalmon'),
    "x": cs('|', 'Red2')+bold('x').cs('Red2')+cs('|', 'Red2'),
}

def _no_colors(m:str) -> str:
    # https://stackoverflow.com/a/38662876
    return re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]').sub('',m)

def _choose_logo(name:str) -> str:
    return LOGOS[name]

class _:
    def __init__(self,colors:bool=True,_raise:bool=False) -> None:        
        self.colors = colors
        self._raise = _raise

    def r(self,e:Exception,cont:bool=False,logo="Exception") -> exit:
        """Raiser"""
        if self._raise:
            raise e
        self.p(f"""{e.__class__.__name__}: {e}""",logo=logo)
        if not cont:
            exit()

    def p(self,message:str,logo:str=None,ext:bool=False) -> print:
        """Printer"""
        message = f"{_choose_logo(logo)} {message}" if logo else message
        print(message if self.colors else _no_colors(message))
        if ext:
            exit()