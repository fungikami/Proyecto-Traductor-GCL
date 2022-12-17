"""
    Funciones misceláneas

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 22/11/2022
"""

from PreAppTable import *

# ------------------------------------
def crossProduct(list):
    ''' Devuelve un string de la forma T1 x (T2 x (T3 x ...)) '''
    if len(list) == 1:
        return list[0]
    else:
        return f'({CROSSPROD} {crossProduct(list[1:])} {list[0]})'

def compose(list):
    ''' Devuelve un string de la forma T1 o (T2 o (T3 o ...)) '''
    if len(list) == 1:
        return list[0]
    else:
        return f'({CIRC} {compose(list[1:])} {list[0]})'