""" 
    Implementación de un analizador léxico para el lenguaje GCL.
    Para ello, se utiliza la librería PLY (Python Lex-Yacc).

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 28/10/2022
"""

from ply.lex import lex
from sys import argv

# Palabras reservadas del lenguaje (Duda de si éstas son las palabras reservadas)
reserved = {
    'true' : 'TkTrue',
    'false' : 'TkFalse',
    'declare' : 'TkDeclare',
    'int' : 'TkInt',
    'bool' : 'TkBool',
    'array' : 'TkArray',
    'if' : 'TkIf',
    'fi' : 'TkFi',
    'do' : 'TkDo',
    'od' : 'TkOd',
    'for' : 'TkFor',
    'rof' : 'TkRof',
    'in' : 'TkIn',
    'to' : 'TkTo',
    'skip' : 'TkSkip',
    'print' : 'TkPrint',
}

# Tokens del lenguaje
tokens = [
    'TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar',
    'TkAsig', 'TkSemicolon', 'TkArrow', 'TkGuard', 'TkPlus', 'TkMinus', 'TkMult', 
    'TkOr', 'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 
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
t_TkGuard = r'\[\]'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkMult = r'\*'
t_TkOr = r'\\/'
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
    r'[_a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'TkId')
    return t

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String que comienza y cierra con comillas dobles. Si se encuentra un \
# ésta debe ser seguida por un " o un \ o un , o un n, de otra manera error.
def t_TkString(t):
    r'\"([^\\\n]|\\\"|\\\\|\\n|\\,)*?\"'
    t.value = t.value[1:-1]
    return t

# Comentarios de tipo: // Esto es un comentario. Debe ser ignorado.
def t_comment(t):
    r'//.*'
    pass
    
# Regla para contar el número de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores: frases incorrectas o mal formadas
def t_error(t):
    column = find_column(data, t)
    print("Error: Unexpected character \"%s\" in row %d, column %d" % (t.value[0], t.lineno, column))
    invalid_tokens.append(t.value[0])
    t.lexer.skip(1)

# Calcula la columna en la que se encuentra el token
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

if __name__ == '__main__':
    # Construir el lexer
    lexer = lex()

    # Leer el archivo de entrada
    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        print("Usage: python lexer.py <input_file>")
        exit(1)
    
    if not argv[1].endswith(".gcl"):
        print("Error: Invalid file extension (must be .gcl)")
        print("Usage: python lexer.py <input_file>")
        exit(1)

    global data
    f = open(argv[1], 'r')
    data = f.read()
    f.close()

    # Tokenizar
    lexer.input(data)

    # Tokens inválidos
    global invalid_tokens
    invalid_tokens = []

    # Imprimir los tokens
    valid_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break

        column = find_column(data, tok)
        if tok.type == 'TkId':
            valid_tokens.append("TkId(\"%s\") %d %d" % (tok.value, tok.lineno, column))
            continue
        if tok.type == 'TkNum':
            valid_tokens.append("TkNum(%d) %d %d" % (tok.value, tok.lineno, column))
            continue

        valid_tokens.append("%s %d %d" % (tok.type, tok.lineno, column))

    # Imprimir los tokens válidos
    if len(invalid_tokens) == 0:
        for token in valid_tokens:
            print(token)
