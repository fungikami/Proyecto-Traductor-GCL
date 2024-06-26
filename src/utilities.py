"""
    Funciones misceláneas

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 22/11/2022
"""

from PreAppTable import *

def getTypePreApp(var):
    ''' Devuelve el tipo de una variable en PreApp '''
    if var == INT:
        return INTSET 
    elif var == BOOL:
        return BOOLSET
    elif var == STR:
        return 
    else:
        # Extrae los números del tipo: array[N..M]
        n = convertNumberPreApp(var[6:var.index('..')])
        m = convertNumberPreApp(var[var.index('..')+2:-1])
        range = f'({RANGEARRAY} {m} {n})'
        return f'({SUPERSCRIPT} {range} {INTSET})'

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

def crossProductRange(list):
    ''' Devuelve un string de la forma (T1 x ...) x (T3 x ...) '''
    cp = crossProduct(list)
    return f'({CROSSPROD} {cp} {cp})'

def crossProductRange2(preApp):
    ''' Devuelve un string de la forma (T1 x ...) x (T3 x ...) '''
    return f'({CROSSPROD} {preApp} {preApp})'

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

def inRangePreApp(var, type, isIn = True):
    ''' Devuelve un string de la forma (x : T) '''
    if isIn:
        return f'(\lambda {var} . {type})'
    return f'(\lambda {var} . {type})'

def notInPreApp(var, type):
    ''' Devuelve un string de la forma x in T '''
    return f'({NOT} ({PAREN} ({IN} {type} {var})))'

def convertNumberPreApp(number):
    ''' Devuelve un string de la forma 123 '''
    num = str(number)
    return convertNumberPreAppAux(num)

def convertNumberPreAppAux(num):
    if len(num) == 1:
        if num == '-':
            return MINUS
        return INTDICT[int(num)]

    return f'({CONCAT} {convertNumberPreAppAux(num[0])} {convertNumberPreAppAux(num[1:])})'
    
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

def existPreApp(var, range, body):
    ''' Devuelve un string de la forma (exists x : | body )'''
    if range is None:
        return f'({EXIST1} (\lambda {var} . {body}))'

    return f'({EXIST2} (\lambda {var} . {range}) (\lambda {var} . {body}))'

def forAllPreApp(var, range, body):
    ''' Devuelve un string de la forma (exists x : | body )'''
    if range is None:
        return f'({FORALL1} (\lambda {var} . {body}))'

    return f'({FORALL2} (\lambda {var} . {body})) (\lambda {var} . {range})'

def anidateExistPreApp(vars, body):
    ''' Devuelve un string de la forma (exists x1 : | (exists x2 : | body )'''
    if len(vars) == 1:
        return existPreApp(vars[0], None, body)

    return existPreApp(vars[0], None, anidateExistPreApp(vars[1:], body))

def equalPreApp(var, value):
    ''' Devuelve un string de la forma (x = 123) '''
    return f'({EQUAL} {value} {var})'

def binOpPreApp(op, a, b):
    ''' Devuelve un string de la forma a op b '''
    return f'({op} {b} {a})'

def setPreApp(range, body):
    ''' Devuelve un string de la forma {range | body} o {body}'''
    if range == None:
        return f'({SET2} {body})'
    return f'({SET1} {body} {range})'

def identityFun(esp):
    ''' 
        Devuelve la función identidad de forma id_esp donde esp es de la forma
        (T1 x T2 x ... x Tn) 
    '''
    return f'({IDENTITY} {esp})'

def espPrima(esp):
    ''' 
        Devuelve el espacio prima de un espacio Ti donde esp es de la forma
        [{x: [T1, x1]}, {y: [T2, x2]}, ...
    '''
    abort = f'({SET2} {ABORT})'
    espPrima = f'({CUP} {abort} {crossProduct(getListEsp(esp))})'
    return espPrima
