from stringcolor import *

def Python():
    return cs('|', 'DeepSkyBlue5')+bold('§').cs('LightGoldenrod2', 'DeepSkyBlue5')+cs('|', 'LightGoldenrod2')+' '

def Excel():
    return cs('|', 'Green4')+cs('X', 'White', 'Green4')+cs('|', 'Green4')+' '

def Json():
    return cs('{', 'Purple5').bold()+cs('j', 'DeepSkyBlue4').bold()+cs('}', 'Purple5').bold()+' '

def Instagram():
    return cs('|', 'LightSalmon2')+cs('o', 'White', 'DeepPink4')+cs('|', 'MediumOrchid')+' '

def Requests():
    return cs('|', 'SeaGreen2')+bold('$').cs('White', 'DarkGrey')+cs('|', 'LightSalmon')+' '

def CSV():
    return cs('|', 'Orange')+bold('c').cs('White', 'Orange')+cs('|', 'Orange')+' '

def i():
    return cs('|', 'DodgerBlue2')+bold('i').cs('White', 'DodgerBlue2')+cs('|', 'DodgerBlue2')+' '

def Exception():
    return cs('|', 'Red2')+bold('!').cs('White', 'Red2')+cs('|', 'Red2')+' '

def Interrrogation():
    return cs('|', 'Violet')+bold('?').cs('White', 'Violet')+cs('|', 'Violet')+' '

def Plus():
    return cs('|', 'DarkSeaGreen9')+bold('+').cs('DarkSeaGreen9', 'White')+cs('|', 'DarkSeaGreen9')+' '

def x():
    return cs('|', 'Red2')+bold('x').cs('Red2')+cs('|', 'Red2')+' '

def compare():
    return cs('|', 'DeepSkyBlue7')+bold('≈').cs('White', 'DeepSkyBlue7')+cs('|', 'DeepSkyBlue7')+' '

def outExcept(e):
    print(Exception()+e)
    exit()

def logo(L):
    mainL = '~'+cs(' Sterra 2.1 ', 'MediumPurple6')+'~'+cs(' made by ', 'MediumPurple6')+bold(cs('aet', 'MediumPurple6'))+cs(' € https://github.com/novitae/sterra ', 'MediumPurple6')+'~'+cs(' GPL-3 ', 'MediumPurple6')+'~'
    logos = {
        'export': '~'+cs(' Export Submodule ', 'MediumPurple6')+'~ '+''.join([str(bold(cs(l, ['DodgerBlue2', 'SlateBlue2', 'SlateBlue', 'Pink4', 'LightPink3', 'SandyBrown', 'Gold', 'Yellow2', 'Yellow'][i], 'Black'))) for i, l in enumerate('instagram')])+' --> ( '+' | '.join([str(bold(cs(l, 'White', ['Green4', 'DarkOrange', 'Purple5'][i]))) for i, l in enumerate(['excel', 'csv', 'json'])])+' ) ~'+cs(' @#S%?*+;:- ', 'MediumPurple6')+'~',
        'compare': '~'+cs(' Compare Submodule ', 'MediumPurple6')+'~ '+f'{Excel()}{CSV()}{Json()}== != <= {Json()}{CSV()}{Excel()}'+'~'+cs(' @#$S%?*+;:-,. ', 'MediumPurple6')+'~',
        'analyse': '~'+cs(' Analyse Submodule ', 'MediumPurple6')+'~ '+f'{Excel()}--> :'+underline(cs('nt(x[\'%\'])>self.p];return s[:e', 'White', 'DarkGreen'))+': ~'+cs(' #%*;- ', 'MediumPurple6')+'~',
        'history': '~'+cs(' History Submodule ', 'MediumPurple6')+'~ '+f'36:28->"PATH", 16:34:57->"PATH", 03:12:4'+' ~'+cs(' #%*;- ', 'MediumPurple6')+'~',
        'convert': '~'+cs(' Convert Submodule ', 'MediumPurple6')+'~ '+f' {Excel()}-->{CSV()}-->{Json()}-->{Excel()}-->{CSV()}-->{Json()} '+'~'+cs(' #%*;- ', 'MediumPurple6')+'~',
    }
    return mainL+'\n'+logos[L]