"""
    Funciones misceláneas

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 22/11/2022
"""

from PreAppTable import *

def getListEsp(listDict):
    ''' Devuelve una lista de los espacios [T1, T2, ...] de una lista de diccionarios 
        de la forma [{'x': ['T1', x_1]}, {'y': ['T2', x_2]}, ...] 
    '''
    esps = []
    for dic in listDict:
        values = dic.values()
        for value in values:
            esps.append(value[0])
    return esps

def getListVar(listDict):
    ''' Devuelve una lista de las variables [x1, x2, ...] de una lista de diccionarios 
        de la forma [{'x': ['T1', x_1]}, {'y': ['T2', x_2]}, ...] 
    '''
    vars = []
    for dic in listDict:
        values = dic.values()
        for value in values:
            vars.append(value[1])
    return vars

def sustitution(list, var, newValue):
    ''' Devuelve una lista de variables tras una sustitución '''
    copyList = list.copy()
    pos = list.index(var)
    copyList[pos] = newValue
    return copyList

def crossProduct(list):
    ''' Devuelve un string de la forma T1 x (T2 x (T3 x ...)) '''
    if len(list) == 1:
        return list[0]
    return f'({CROSSPROD} {crossProduct(list[1:])} {list[0]})'

def crossProductPreApp(list):
    ''' Devuelve un string de la forma (T1 x ...) x (T3 x ...) '''
    cp = crossProduct(list)
    return f'({CROSSPROD} {cp} {cp})'

def compose(list):
    ''' Devuelve un string de la forma T1 o (T2 o (T3 o ...)) '''
    if len(list) == 1:
        return list[0]
    return f'({CIRC} {compose(list[1:])} {list[0]})'

def composePi(list, semS):
    ''' Devuelve un string de la forma pi o pi o ... o semS '''
    if len(list) == 1:
        return semS 

    # Calcula cuantos pi's hay que agregar
    m = 0
    for i in range(len(list)):
        m += len(list[i])
    n = m - len(list[-1])
    pis = [PI] * (m - n)
    return compose(pis + [semS])

def inPreApp(var, type):
    ''' Devuelve un string de la forma (x : T) '''
    return f'(\lambda {var} . {type})'

def convertNumberPreApp(number):
    ''' Devuelve un string de la forma 123 '''
    num = str(number)
    return convertNumberPreAppAux(num)

def convertNumberPreAppAux(num):
    if len(num) == 1:
        return INTDICT[int(num)]
    return f'({CONCAT} {INTDICT[int(num[0])]} {convertNumberPreAppAux(num[1:])})'
    
def convertBooleanPreApp(boolean):
    return BOOLDICT[boolean]

def coordenatesPreApp(list):
    ''' Devuelve un string de la forma (x1, x2, ..., xn) '''
    return f'({PAREN} {coordenatesPreAppAux(list)})'

def coordenatesPreAppAux(list):
    if len(list) == 1:
        return list[0]
    return f'({COMMA} {coordenatesPreAppAux(list[1:])} {list[0]})'

def tuplePreApp(l, r):
    ''' Devuelve un string de la forma <l, r> '''
    return f'({TUPLE} {r} {l})'

def existPreApp(var, body):
    ''' Devuelve un string de la forma (exists x : | body )'''
    return f'({EXIST1} (\lambda {var} . {body}))'

def anidateExistPreApp(vars, body):
    ''' Devuelve un string de la forma (exists x1 : | (exists x2 : | body )'''
    if len(vars) == 1:
        return existPreApp(vars[0], body)

    return existPreApp(vars[0], anidateExistPreApp(vars[1:], body))

def equalPreApp(var, value):
    ''' Devuelve un string de la forma (x = 123) '''
    return f'({EQUAL} {value} {var})'

def setPreApp(range, body):
    ''' Devuelve un string de la forma {range | body} o {body}'''
    if range == None:
        return f'({SET2} {body})'
    return f'({SET1} {body} {range})'
