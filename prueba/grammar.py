"""
    Reglas gramaticales para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from AST import *
from lexer import tokens

# Reglas de precedencia (Por revisar)
precedence = (
    ('nonassoc', 'TkOBlock', 'TkCBlock'),
    ('nonassoc', 'TkSkip'),
    ('nonassoc', 'TkPrint'),
    ('nonassoc', 'TkIf'),
    ('nonassoc', 'TkFor'),
    ('nonassoc', 'TkDo'),
    ('nonassoc', 'TkId'),
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

# Definicion de la gramatica
# Programa es un bloque
def p_program(p):
    """program : block"""
    p[0] = p[1]

# Bloque (Preguntar si es válido un bloque vacío)
# <block> -> |[ <declarations> <instructions> ]|
def p_block(p):
    """block : TkOBlock declarations instructions TkCBlock"""
    p[0] = Block(p[2], p[3])

# Declaraciones
# <declarations> -> declare <sec_declarations>
#                | λ
def p_declarations(p):
    """declarations : TkDeclare seq_declarations
                    | lambda"""
    p[0] = Declare(p[2] if len(p) == 3 else p[1])

# Secuencia de declaraciones
# <sec_declarations>  -> <declaration>; <sec_declarations>
#                      | <declaration>
def p_seq_declarations(p):
    """seq_declarations : declaration TkSemicolon seq_declarations
                        | declaration"""
    if len(p) == 4:
        p[0] = Sequencing(p[1], p[3])
    else:
        p[0] = p[1]

# Declaración
# <declaration> -> <idLists> : <type>
def p_declaration(p):
    """declaration : idLists TkTwoPoints type"""
    p[0] = Declaration(p[1], p[3])

# Lista de identificadores
# <idLists> -> <id>, <idLists>
#            | <id>
def p_idLists(p):
    """idLists : id TkComma idLists
               | id"""

    if len(p) == 4:
        p[0] = IdLists(p[1], p[3])
    else:
        p[0] = p[1]

# Instrucciones
# <instructions> -> <instructions>, <instruction>;
#                 | <instruction>
def p_instructions(p):
    """instructions : instructions TkSemicolon instruction 
                    | instruction"""
    if len(p) == 4:
        p[0] = Sequencing(p[1], p[3])
    else:
        p[0] = p[1]

# Instrucción
# <instruction>  -> skip
#                |  <assignment>
#                |  <print_instruction>
#                |  <conditional>
#                |  <forLoop>
#                |  <doLoop>
def p_instruction(p):
    """instruction : TkSkip
                   | assignment
                   | print_instruction
                   | conditional
                   | for
                   | do"""
    p[0] = Skip() if p[1] == 'skip' else p[1]

# Asignación
# <assignment> -> <id> := <expression>
#               | <id> := <array_expr>
def p_assignment(p):
    """assignment : id TkAsig expression
                  | id TkAsig array_expr"""
    p[0] = Asig(p[1], p[3])

binary = {
    '+': Plus,
    '-': Minus,
    '*': Mult,
    '/\\': And,
    '\/': Or,
    '==': Equal,
    '!=': NEqual,
    '<': Less,
    '<=': Leq,
    '>': Greater,
    '>=': Geq,
}

# Expresiones binarias
#                 -> <expression> + <expression>
#                  | <expression> - <expression>
#                  | <expression> * <expression>
#                  | <expression> \/ <expression>
#                  | <expression> /\ <expression>
#                  | <expression> < <expression>
#                  | <expression> <= <expression>
#                  | <expression> >= <expression>
#                  | <expression> > <expression>
#                  | <expression> == <expression>
#                  | <expression> != <expression>
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

# Expresiones unarias
# <expression>    -> (<expression>)
#                  | -<expression>
#                  | !<expression>
def p_unary_expression(p):
    """expression : TkMinus expression %prec UNARY
                  | TkNot expression %prec UNARY"""
    if p[1] == '-':
        p[0]= UnaryMinus(p[2])
    else:
        p[0] = Neg(p[2])

# Expresiones terminales
# <expression>    -> (<expression>)
#                  | <int_array_access>
#                  | <int_array_modify>
#                  | <number>
#                  | <boolean>
#                  | <id>
def p_terminal_expression(p):
    """expression : TkOpenPar expression TkClosePar
                  | int_array_access
                  | int_array_modify
                  | number
                  | boolean
                  | id"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

# Expresiones de arreglos
# <array_expr> -> <int_array>
def p_array_expr(p):
    """array_expr : int_array"""
    p[0] = p[1]

# Arreglo de enteros
# <int_array> -> <number>, <int_array>
#               | <number>
def p_int_array(p):
    """int_array : expression TkComma int_array
                 | expression"""
    if len(p) == 4:
        p[0] = Comma(p[1], p[3])
    else:
        p[0] = p[1]

# Acceso a un elemento de un arreglo
# <int_array_access> -> <id>[<expression>]
def p_int_array_access(p):
    """int_array_access : id TkOBracket expression TkCBracket"""
    p[0] = ReadArray(p[1], p[3])

# Modificación de un elemento de un arreglo
# <int_array_modify> -> <id><expression>
def p_int_array_modify(p):
    """int_array_modify : expression TkOpenPar expression TkTwoPoints expression TkClosePar"""
    p[0] = WriteArray(p[1], TwoPoints(p[3], p[5]))

# Salida
# <print_instruction> -> print <concatenation>
def p_print_instruction(p):
    """print_instruction : TkPrint concatenation"""
    p[0] = Print(p[2])

# Concatenación
# <concatenation> -> <string_expression> . <concatenation>
#                  | <string_expression> 
def p_concatenation(p):
    """concatenation : string_expression TkConcat concatenation
                     | string_expression"""
    if len(p) == 4:
        p[0] = Concat(p[1], p[3])
    else:
        p[0] = p[1]

# Expresión de cadena
# <string_expression>  -> <expresion> 
#                       | <string>
def p_string_expression(p):
    """string_expression : expression
                         | string"""
    p[0] = p[1]

# Condicionales
# <conditional>   -> if <guards> fi
def p_conditional(p):
    """conditional : TkIf guards TkFi"""
    p[0] = If(p[2])

# Guardias
# <guards> -> <guard> 
#           | <guard> [] <guards>
def p_guards(p):
    """guards : guards TkGuard guard
                | guard"""
    if len(p) == 4:
        p[0] = Guard(p[1], p[3])
    else:
        p[0] = p[1]

# Guardia
# <guard> -> <expression> --> <execute>
def p_guard(p):
    """guard : expression TkArrow execute """
    p[0] = Then(p[1], p[3])

# Ejecución
# <execute>   -> <instructions>
#              | <block>
def p_execute(p):
    """execute : instructions
               | block"""
    p[0] = p[1]

# Ciclos for
# <forLoop> -> for <id> in <expression> to <expression> --> <execute> rof
def p_for(p):
    """for : TkFor id TkIn expression TkTo expression TkArrow execute TkRof"""
    p[0] = For(In(p[2], To(p[4], p[6])), p[8])

# Ciclos do
# <doLoop> -> do <expression> --> <execute> od
def p_do(p):
    """do : TkDo expression TkArrow execute TkOd"""
    p[0] = Do(Then(p[2], p[4]))

# Terminales
# Tipos
# <type>  -> int
#          | bool
#          | array[<number> .. <number>]
def p_type(p):
    """type : TkInt
            | TkBool
            | TkArray TkOBracket number TkSoForth number TkCBracket"""
    if len(p) == 2:
        p[0] = Type(p[1])
    else:
        p[0] = ArrayType(p[3], p[5])

# Identificadores
# <id>    -> [a-zA-Z_][a-zA-Z_]*
def p_id(p):
    """id : TkId"""
    p[0] = Id(p[1])

# Números
# <number>    -> [0-9]+
def p_number(p):
    """number : TkNum"""
    p[0] = Number(p[1])

# Booleanos
# <boolean>   -> true
#              | false
def p_boolean(p):
    """boolean : TkTrue
               | TkFalse"""
    p[0] = Boolean(p[1])

# Cadenas
# <string>    -> "([^\n\]|\"|\\|\n)*"
def p_string(p):
    """string : TkString"""
    p[0] = String(p[1])

def p_lambda(p):
    """lambda :"""
    pass

# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Error: Sintax error in row %d, column %d: unexpected token '%s'." % (
            p.lineno, p.lexpos + 1, p.value))
    else:
        print("Error: Unexpected end of input")
