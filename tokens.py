""" 
    Documentación

"""

import re
from ply.lex import LexToken

# Palabras reservadas del lenguaje (Duda de si éstas son las palabras reservadas)
reserved = {
    'true' : 'TkTrue',
    'false' : 'TkFalse',
}

# Tokens del lenguaje
tokens = [
    'TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar',
    'TkAsig', 'TkSemicolon', 'TkArrow', 'TkPlus', 'TkMinus', 'TkMult', 'TkOr', 
    'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 'TkGef', 'TkGreater', 'TkEqual', 
    'TkNEqual', 'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkConcat',
]

tokens += list(reserved.values())

# Ignorar espacios, tabulaciones y saltos de línea 
t_ignore = ' \t'

# Expresiones regulares para tokens simples
t_TkOBlock = r'\|\['       
t_TkCBlock = r'\]\|'
t_TkSoForth = r'\.\.'
t_TkComma = r','
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkAsig = r':='
t_TkSemicolon  = r';'
t_TkArrow = r'-->'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkMult = r'\*'
t_TkOr = r'\/'
t_TkAnd = r'/\\'
t_TkNot = r'!'
t_TkLess = r'<'
t_TkLeq = r'<='
t_TkGeq = r'>='
t_TkGreater = r'>'
t_TkEqual = r'=='
t_TkNEqual = r'!='
t_TkOBracket = r'\['
t_TkCBracket = r'\]'
t_TkTwoPoints = r':'  
t_TkConcat = r'\.'

# Expresiones regulares para dígitos, caracteres... 
def t_TkId(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'TkId')
    return t

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Comentarios de tipo: // Esto es un comentario. Debe ser ignorado.
def t_comment(t):
    r'//.*'
    pass

# Errores: frases incorrectas o mal formadas
def t_error(t):
    return "to-do"
