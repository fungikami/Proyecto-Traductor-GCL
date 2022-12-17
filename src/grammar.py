"""
    Reglas gramaticales para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from AST import *
from lexer import tokens

# Reglas de precedencia
precedence = (
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('left', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),
    ('nonassoc', 'UNOT'),
    ('left', 'TkEqual', 'TkNEqual'),
    ('right', 'TkNot'),
    ('nonassoc', 'TkTwoPoints'),
    ('left', 'TkComma'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkMult'),
    ('nonassoc', 'UMINUS'),
    ('nonassoc', 'TkOBlock', 'TkCBlock', 'TkOBracket', 'TkCBracket', 'TkOpenPar', 'TkClosePar'),
)

# --------------------- PROGRAM ---------------------
def p_program(p):
    """program : block"""
    p[0] = Program(p[1], p[1].row, p[1].column)

# --------------------- BLOCK ---------------------
# <block> -> |[ <declarations> <instructions> ]|
def p_block(p):
    """block : TkOBlock declarations instructions TkCBlock"""
    p[0] = Block(p[2], p[3], p.lineno(1), find_column(p.lexer.lexdata, p))

# --------------------- DECLARE ---------------------
# <declarations> -> declare <sec_declarations>
#                | λ
def p_declarations(p):
    """declarations : TkDeclare seq_declarations
                    | lambda"""
    p[0] = Declare(p[2] if len(p) == 3 else p[1], p.lineno(1), find_column(p.lexer.lexdata, p))

# Secuencia de declaraciones
# <sec_declarations>  -> <sec_declarations>, <declaration>;
#                      | <declaration>
def p_seq_declarations(p):
    """seq_declarations : seq_declarations TkSemicolon declaration
                        | declaration"""
    if len(p) == 4:
        p[0] = Sequencing(p[1], p[3], p[1].row, p[1].column)
    else:
        p[0] = p[1]

# Declaración
# <declaration> -> <idLists> : <type>
def p_declaration(p):
    """declaration : idLists TkTwoPoints type"""
    p[0] = Declaration(p[1], p[3], p[1][0].row, p[1][0].column)

# Lista de identificadores
# <idLists> -> <id>, <idLists>
#            | <id>
def p_idLists(p):
    """idLists : id TkComma idLists
               | id"""
    if len(p) == 4:
        p[0] = [p[1], *p[3]]
    else:
        p[0] = [p[1]]

# --------------------- INSTRUCTIONS ---------------------
# <instructions> -> <instructions>, <instruction>;
#                 | <instruction>
def p_instructions(p):
    """instructions : instructions TkSemicolon instruction 
                    | instruction"""
    if len(p) == 4:
        p[0] = Sequencing(p[1], p[3], p[1].row, p[1].column)
    else:
        p[0] = p[1]

# Instrucción
# <instruction>  -> skip
#                |  <assignment>
#                |  <print_instruction>
#                |  <conditional>
#                |  <forLoop>
#                |  <doLoop>
#                |  <block>
def p_instruction(p):
    """instruction : TkSkip
                   | assignment
                   | print_instruction
                   | conditional
                   | for
                   | do
                   | block"""
    p[0] = Skip(p.lineno(1), find_column(p.lexer.lexdata, p)) if p[1] == 'skip' else p[1]

# --------------------- ASSIGNMENT ---------------------
# <assignment> -> <id> := <expression>
def p_assignment(p):
    """assignment : id TkAsig expression"""
    p[0] = Asig(p[1], p[3], p[1].row, p[1].column)

# --------------------- BINARY OPERATORS ---------------------
# <expression> -> <expression> + <expression>
#               | <expression> - <expression>
#               | <expression> * <expression>
#               | <expression> \/ <expression>
#               | <expression> /\ <expression>
#               | <expression> < <expression>
#               | <expression> <= <expression>
#               | <expression> >= <expression>
#               | <expression> > <expression>
#               | <expression> == <expression>
#               | <expression> != <expression>
#               | <expression> , <expression>
binary = {
    '+': Plus, '-': Minus, '*': Mult,
    '/\\': And, '\/': Or,
    '==': Equal, '!=': NEqual,
    '<': Less, '<=': Leq,
    '>': Greater, '>=': Geq,
    ',': Comma,
}

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
                  | expression TkNEqual expression
                  | expression TkComma expression"""
    p[0] = binary[p[2]](p[1], p[3], p[1].row, p[1].column)

# --------------------- UNARY OPERATORS ---------------------
# <expression>    -> -<expression>
#                  | !<expression>
def p_unary_expression(p):
    """expression : TkMinus expression %prec UMINUS
                  | TkNot expression %prec UNOT"""
    if p[1] == '-':
        p[0]= UnaryMinus(p[2], p.lineno(1), find_column(p.lexer.lexdata, p))
    else:
        p[0] = Not(p[2], p.lineno(1), find_column(p.lexer.lexdata, p))

# --------------------- TERMINAL EXPRESSIONS ---------------------
# <expression>    -> (<expression>)
#                  | <array_access>
#                  | <array_modify>
#                  | <number>
#                  | <boolean>
#                  | <id>
def p_terminal_expression(p):
    """expression : TkOpenPar expression TkClosePar
                  | array_access
                  | array_modify
                  | number
                  | boolean
                  | id
                  | string """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

# --------------------- ARREGLOS ---------------------
# Acceso a un elemento de un arreglo
# <array_access> -> <expression>[<expression>]
def p_array_access(p):
    """array_access : expression TkOBracket expression TkCBracket"""
    p[0] = ReadArray(p[1], p[3], p[1].row, p[1].column)

# Modificación de un elemento de un arreglo
# <array_modify> -> <expression>(<expression>:<expression>)
def p_array_modify(p):
    """array_modify : expression TkOpenPar expression TkTwoPoints expression TkClosePar"""
    p[0] = WriteArray(p[1], TwoPoints(p[3], p[5], p[1].row, p[1].column), p[1].row, p[1].column)

# --------------------- PRINT ---------------------
# <print_instruction> -> print <concatenation>
def p_print_instruction(p):
    """print_instruction : TkPrint concatenation"""
    p[0] = Print(p[2], p.lineno(1), find_column(p.lexer.lexdata, p))

# <concatenation> -> <concatenation> . <expression>
#                  | <expression> 
def p_concatenation(p):
    """concatenation : concatenation TkConcat expression
                     | expression"""
    if len(p) == 4:
        p[0] = Concat(p[1], p[3], p[1].row, p[1].column)
    else:
        p[0] = p[1]

# --------------------- CONDICIONAL ---------------------
# <conditional>   -> if <guards> fi
def p_conditional(p):
    """conditional : TkIf guards TkFi"""
    p[0] = If(p[2], p.lineno(1), find_column(p.lexer.lexdata, p))

# Guardias
# <guards> -> <guards> [] <guard>
#           | <guard> 
def p_guards(p):
    """guards : guards TkGuard guard
                | guard"""
    if len(p) == 4:
        p[0] = Guard(p[1], p[3], p[1].row, p[1].column)
    else:
        p[0] = p[1]

# Guardia
# <guard> -> <expression> --> <instructions>
def p_guard(p):
    """guard : expression TkArrow instructions """
    p[0] = Then(p[1], p[3], p[1].row, p[1].column)

# --------------------- FOR LOOP ---------------------
# <forLoop> -> for <id> in <expression> to <expression> --> <instructions> rof
def p_for(p):
    """for : TkFor id TkIn expression TkTo expression TkArrow instructions TkRof"""
    row = p.lineno(1)
    col = find_column(p.lexer.lexdata, p)
    p[0] = For(In(p[2], To(p[4], p[6], row, col), row, col), p[8], row, col)

# --------------------- DO LOOP ---------------------
# <doLoop> -> do <guards> od
def p_do(p):
    """do : TkDo guards TkOd"""
    p[0] = Do(p[2], p.lineno(1), find_column(p.lexer.lexdata, p))

# --------------------- TYPES ---------------------
# <type>  -> int
#          | bool
#          | array[<expression> .. <expression>]
def p_type(p):
    """type : TkInt
            | TkBool
            | TkArray TkOBracket expression TkSoForth expression TkCBracket"""
    if len(p) == 2:
        p[0] = Type(p[1], p.lineno(1), find_column(p.lexer.lexdata, p))
    else:
        p[0] = ArrayType(p[3], p[5], p.lineno(1), find_column(p.lexer.lexdata, p))

# --------------------- TERMINALS ---------------------
# Identificadores
# <id>    -> [a-zA-Z_][a-zA-Z_]*
def p_id(p):
    """id : TkId"""
    p[0] = Id(p[1], p.lineno(1), find_column(p.lexer.lexdata, p))

# Números
# <number>    -> [0-9]+
def p_number(p):
    """number : TkNum"""
    p[0] = Number(p[1], p.lineno(1), find_column(p.lexer.lexdata, p))

# Booleanos
# <boolean>   -> true
#              | false
def p_boolean(p):
    """boolean : TkTrue
               | TkFalse"""
    p[0] = Boolean(p[1], p.lineno(1), find_column(p.lexer.lexdata, p))

# Cadenas
# <string>    -> "([^\n\]|\"|\\|\n)*"
def p_string(p):
    """string : TkString"""
    p[0] = String(p[1], p.lineno(1), find_column(p.lexer.lexdata, p))

def p_lambda(p):
    """lambda :"""
    pass

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos(1)) + 1
    return (token.lexpos(1) - line_start) + 1

# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Sintax error in row %d, column %d: unexpected token '%s'." % (
            p.lineno, find_column(p.lexer.lexdata, p), p.value))
    else:
        print("Unexpected end of input")
