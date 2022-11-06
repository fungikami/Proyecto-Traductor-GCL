"""
    Reglas gramaticales para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from . import AST

# Reglas de precedencia (Por revisar)
precedence = (
    ('nonassoc', 'TkAsig'),
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    
    ('left', 'TkEqual', 'TkNEqual'),
    ('left', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),

    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult'),

    ('right', 'TkNot'),
)

# Definicion de la gramatica
# Bloque
def p_block(p):
    'block : TkOBlock TkCBlock'
    p[0] = AST.Block([])

def p_instr(p):
    '''instr : block
             | skip
             | seq
             | asig
             | print
             | if
             | while
             | for
             | case
             | call
             | return'''
    p[0] = p[1]

# Skip
def p_skip(p):
    'skip : TkSkip'
    p[0] = AST.Skip()

# Secuenciacion
def p_seq(p):
    'seq : seq TkSemicolon instr'
    p[0] = AST.Seq(p[1], p[3])

# Asignacion
def p_asig(p):
    'asig : TkId TkAsig exp'
    p[0] = AST.Asign(p[1], p[3])

# Print print "Hola " . "mundo! " . 1 . "\n"
def p_print(p):
    'print : TkPrint exp'
    p[0] = AST.Print(p[2])

# Condicionales
# if <condición1> --> <instrucción1> [] <condición2> --> <instrucción2> [] <condiciónN> --> <instrucciónN> fi
def p_if(p):
    'if : TkIf TkOBlock TkCBlock TkFi'
    p[0] = AST.If([])

# Iteraciones do <condición> --> <instrucción> od
def p_while(p):
    'while : TkDo TkOBlock TkCBlock TkOd'
    p[0] = AST.While([])

# Iteraciones con multiples guardias
def p_for(p):
    'for : TkFor TkOBlock TkCBlock TkRof'
    p[0] = AST.For([])

# Expresiones
def p_exp(p):
    "to-do"

# Expresiones terminales
def p_exp_term(p):
    '''expr : TkId
            | TkNum
            | TkTrue
            | TkFalse
            | TkStr'''
    p[0] = p[1]

# Expresiones unarias
def p_exp_unary(p):
    '''expr : TkNot expr
            | TkMinus expr'''
    p[0] = AST.Unary(p[1], p[2])

# Expresiones binarias
def p_exp_binary(p):
    '''expr : expr TkPlus expr
            | expr TkMinus expr
            | expr TkMult expr
            | expr TkOr expr
            | expr TkAnd expr
            | expr TkEqual expr
            | expr TkNEqual expr
            | expr TkLess expr
            | expr TkLeq expr
            | expr TkGeq expr
            | expr TkGreater expr'''
    p[0] = AST.Binary(p[2], p[1], p[3])

# Expresiones con arreglo
def p_exp_array(p):
    'expr : TkId TkOBrack expr TkCBrack'
    p[0] = AST.Array(p[1], p[3])

# Comparacion de expresiones
def p_exp_compare(p):
    '''expr : expr TkEqual expr
            | expr TkNEqual expr
            | expr TkLess expr
            | expr TkLeq expr
            | expr TkGeq expr
            | expr TkGreater expr'''
    p[0] = AST.Compare(p[2], p[1], p[3])

# Expresiones terminales
def p_exp_term(p):
    '''expr : TkId
            | TkNum
            | TkTrue
            | TkFalse
            | TkStr'''
    p[0] = p[1]

# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Error: Sintax error in row %d, column %d: unexpected token '%s'." % (p.lineno, p.lexpos, p.value))
    else:
        print("Error: Unexpected end of input")


    

