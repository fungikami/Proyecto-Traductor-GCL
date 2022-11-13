"""
    Reglas gramaticales para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from AST import AST
from lexer import tokens

# Reglas de precedencia (Por revisar)
precedence = (
    ('nonassoc', 'TkAsig'),
    ('left', 'TkOr'),
    ('left', 'TkAnd'),

    ('left', 'TkEqual', 'TkNEqual'),
    ('left', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),

    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult'),
    ('nonassoc', 'UNARY'),
    ('right', 'TkNot'),

)

# binary = {
#     'TkPlus': AST.Plus,
#     'TkMinus': AST.Minus,
#     'TkMult': AST.Mult,
#     'TkAnd': AST.And,
#     'TkOr': AST.Or,
#     'TkEqual': AST.Equal,
#     'TkNEqual': AST.NEqual,
#     'TkLess': AST.Less,
#     'TkLeq': AST.Leq,
#     'TkGreater': AST.Greater,
#     'TkGeq': AST.Geq,
# }

# Definicion de la gramatica
# Programa es un bloque
def p_program(p):
    """program : block"""
    p[0] = p[1]

# Bloque (Preguntar si es válido un bloque vacío)
# <block> -> |[ <declarations> <instructions> ]|
def p_block(p):
    """block : TkOBlock declaration instructions TkCBlock"""
    p[0] = AST.Block(p[2], p[3])

# Declaraciones
# <declarations> -> declare <sec_declarations>
#                | λ


def p_declarations(p):
    """declarations : TkDeclare seq_declarations
        | lambda"""
    p[0] = AST.Declare(p[2] if len(p) == 3 else p[1])


# Secuencia de declaraciones
# <sec_declarations>  -> <declaration>; <sec_declarations>
#                      | <declaration>
def p_seq_declarations(p):
    """seq_declarations : declaration TkSemicolon seq_declarations
        | declaration"""
    if len(p) == 4:
        p[0] = AST.Sequencing(p[1], p[3])
    else:
        p[0] = p[1]

# Declaración
# <declaration> -> <idLists> : <type>
def p_declaration(p):
    """declaration : idLists TkSemicolon type"""
    p[0] = AST.Declaration(p[1], p[3])

# Lista de identificadores
# <idLists> -> <id> <idLists>
#            | <id>
def p_idLists(p):
    """idLists : id idLists
        | id"""
    p[0] = AST.List(p[1], p[2])

# Instrucciones
# <instructions> -> <instruction>; <instructions>
#   | <instruction>
def p_instructions(p):
    """instructions : instruction TkSemicolon instructions
        | instruction"""
    if len(p) == 4:
        p[0] = AST.Sequencing(p[1], p[3])
    else:
        p[0] = p[1]

# Instrucción
# <instruction>  -> skip
#   |  <assignment>
#   |  <print_instruction>
#   |  <conditional>
#   |  <forLoop>
#   |  <doLoop>
def p_instruction(p):
    """instruction : TkSkip
        | assignment
        | print_instruction
        | conditional
        | for
        | do"""
    p[0] = p[1]

# Asignación
# <assignment> -> <id> := <expression>
def p_assignment(p):
    """assignment : id TkAsig expression"""
    p[0] = AST.Asig(p[1], p[3])

# Expresión
# <expression>    -> (<expression>)
#   | <expression> + <expression>
#   | <expression> - <expression>
#   | <expression> * <expression>
#   | -<expression>
#   | <expression> \/ <expression>
#   | <expression> /\ <expression>
#   | !<expression>
#   | <expression> < <expression>
#   | <expression> <= <expression>
#   | <expression> >= <expression>
#   | <expression> > <expression>
#   | <expression> == <expression>
#   | <expression> != <expression>
#   | <int_array>
#   | <int_array_access>
#   | <number>
#   | <boolean>
#   | <id>
def p_binary_expression(p):
    """expression : expression TkPlus expression
        | expression TkMinus expression
        | expression TkMult expression
        | expression TkOr expression
        | expression TkAnd expression
        | expression TkLess expression
        | expression TkLeq expression
        | expression TkGeq expression
        | expression TkGreater expression
        | expression TkEqual expression
        | expression TkNEqual expression"""
    p[0] = binary[p[2]](p[1], p[3])
def p_unary_expression(p):
    """expression : TkMinus expression %prec UNARY
        | TkNot expression %prec UNARY"""
    if p[1] == '-':
        p[0] = AST.Minus(p[2])
    else:
        p[0] = AST.Neg(p[2])

def p_terminal_expression(p):
    """expression : TkOpenPar expression TkClosePar
        | int_array
        | int_array_access
        | number
        | boolean
        | id"""
    p[0] = p[1]


# Acceso a un elemento de un arreglo
# <int_array_access> -> <id>[<expression>]
def p_int_array_access(p):
    """int_array_access : id TkOBracket expression TkCBracket"""

# Arreglo de enteros
# <int_array> -> [ <int_array_elements> ]
def p_int_array(p):
    """int_array : TkOBracket int_array_elements TkCBracket"""

# Elementos de un arreglo de enteros
# <int_array_elements> -> <number>, <int_array_elements>
#   | <number>
def p_int_array_elements(p):
    """int_array_elements : number TkComma int_array_elements
        | number"""

# Salida
# <print_instruction> -> print <concatenation>
def p_print_instruction(p):
    """print_instruction : TkPrint concatenation"""

# Concatenación
# <concatenation> -> <string_expression> . <concatenation>
#   | <string_expression> 
def p_concatenation(p):
    """concatenation : string_expression TkConcat concatenation
        | string_expression"""

# Expresión de cadena
# <string_expression>  -> <expresion> | <string>
def p_string_expression(p):
    """string_expression : expression
        | string"""

# Condicionales
# <conditional>   -> if <expression> --> <execute> <guards> fi
def p_conditional(p):
    """conditional : TkIf expression TkArrow execute guards TkFi"""

# Guardias
# <guards> -> <guard> | <guard> <guards>
#   | λ
def p_guards(p):
    """guards : guard
        | guard guards
        | lambda"""

# Guardia
# <guard> -> [] <expression> --> <execute>
#   | λ
def p_guard(p):
    """guard : TkGuard expression TkArrow execute
        | lambda"""

# Ejecución
# <execute>   -> <instructions>
#   | <block>
def p_execute(p):
    """execute : instructions
        | block"""

# Ciclos for
# <forLoop> -> for <id> in <expression> to <expression> --> <execute> rof
def p_for(p):
    """for : TkFor id TkIn expression TkTo expression TkArrow execute TkRof"""

# Ciclos do
# <doLoop> -> do <expression> --> <execute> od
def p_do(p):
    """do : TkDo expression TkArrow execute TkOd"""

# Terminales
# Tipos
# <type>  -> int
#   | bool
#   | array[<number> .. <number>]
def p_type(p):
    """type : TkInt
        | TkBool
        | TkArray TkOBracket number TkTwoPoints number TkCBracket"""

# Identificadores
# <id>    -> [a-zA-Z_][a-zA-Z_]*
def p_id(p):
    """id : TkId"""

# Números
# <number>    -> [0-9]+
def p_number(p):
    """number : TkNum"""

# Booleanos
# <boolean>   -> true
#   | false
def p_boolean(p):
    """boolean : TkTrue
        | TkFalse"""

# Cadenas
# <string>    -> "([^\n\]|\"|\\|\n)*"
def p_string(p):
    """string : TkString"""

def p_lambda(p):
    """lambda :"""


# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Error: Sintax error in row %d, column %d: unexpected token '%s'." % (
            p.lineno, p.lexpos, p.value))
    else:
        print("Error: Unexpected end of input")
