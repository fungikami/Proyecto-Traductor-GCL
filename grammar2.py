"""
    Reglas gramaticales para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from AST import AST

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

# Definicion de la gramatica
# Programa es un bloque
# def p_program(p):
#     """program : block"""
#     p[0] = AST("Program", p[1])

# Bloque (Preguntar si es válido un bloque vacío)
# <Block> -> |[ <Declare> <Sequencing> ]|
def p_Block(p):
    """Block : TkOBlock TkDeclare Declare Sequencing TkCBlock
             | TkOBlock Sequencing TkCBlock"""
    p[0] = AST("Block", [p[2], p[3]], [p[1], p[4]])

# Declaracion
# <Declare> -> <Declaration>
#            | <Sequencing>
def p_Declare(p):
    """Declare : declaration
               | declaration TkSemicolon declaration"""
    p[0] = AST("Declare", [p[1]])

# Declaracion
# <Declaration> -> <idLists> : <type>
def p_declaration(p):
    """declaration : idLists TkTwoPoints type"""
    p[0] = AST("Declaration", [p[1], p[3]], p[2])

# Lista de identificadores
# <idLists> -> <id>, <idLists>
#            | <id>
def p_idLists(p):
    """idLists : TkId TkComma idLists
               | TkId"""
    if len(p) == 4:
        p[0] = AST("IdLists", [p[1], p[3]], p[2])
    else:
        p[0] = AST("IdLists", [p[1]])

# Tipo de dato
# <type> -> TkInt
#         | TkBool
#         | TkArray
def p_type(p):
    """type : TkInt
            | TkBool
            | TkArray TkOBracket TkNum TkSoForth TkNum TkCBracket"""
    p[0] = AST("Type", [p[1]])


# Secuenciacion
# <Sequencing> -> <declaration> <declaration>
#             | <instruction> <instruction>
def p_Sequencing(p):
    """Sequencing : declaration TkSemicolon declaration
                  | declaration TkSemicolon instruction
                  | instruction TkSemicolon instruction"""
    p[0] = AST("Sequencing", [p[1], p[3]], p[2])

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
    p[0] = AST("Instruction", [p[1]])

# Asignación
# <assignment> -> <id> := <expression>
def p_assignment(p):
    """assignment : TkId TkAsig expression"""
    p[0] = AST("Assignment", [p[1], p[3]], p[2])

# Booleano
# <bool> -> TkTrue
#         | TkFalse
#         | parethesisBool
def p_bool(p):
    """bool : TkTrue
            | TkFalse
            | parenthesis"""
    p[0] = AST("Bool", [p[1]])

# Expresión
# <expression> -> <expression> + <term>
#               | <expression> - <term>
#               | <term>
#               | <bool>
def p_expression(p):
    """expression : expression TkPlus term
                  | expression TkMinus term
                  | term
                  | bool"""
    if len(p) == 4:
        p[0] = AST("Expression", [p[1], p[3]], p[2])
    else:
        p[0] = AST("Expression", [p[1]])

# Termino
# <term> -> <term> * <factor>
#         | <factor>
def p_term(p):
    """term : term TkMult factor
            | factor"""
    if len(p) == 4:
        p[0] = AST("Term", [p[1], p[3]], p[2])
    else:
        p[0] = AST("Term", [p[1]])

# Factor
# <factor> -> <id>
#           | <int>
#           | <parenthesis>
#           | - <factor>
def p_factor(p):
    """factor : TkId
              | TkNum
              | parenthesis
              | TkMinus factor %prec UNARY"""
    if len(p) == 3:
        p[0] = AST("Factor", [p[2]], p[1])
    else:
        p[0] = AST("Factor", [p[1]])

# Parentesis
# <parenthesis> -> ( <expression> )
def p_parenthesis(p):
    """parenthesis : TkOpenPar expression TkClosePar"""
    p[0] = AST("Parenthesis", [p[2]], [p[1], p[3]])

# Instrucción de impresión
# <print_instruction> -> print <expression>
#                      | print <string>
def p_print_instruction(p):
    """print_instruction : TkPrint expression
                         | TkPrint string"""
    p[0] = AST("PrintInstruction", [p[2]], p[1])

# Cadena de caracteres
# <string> -> TkString
#           | TkString TkConcat <string>
def p_string(p):
    """string : TkString
              | TkString TkConcat string"""
    p[0] = AST("String", [p[1]])

# Condicionales
# <conditional> -> if <expression> then <instruction> else <instruction>
def p_conditional(p):
    """conditional : TkIf"""
    p[0] = AST("Conditional", [p[2], p[4], p[6]], [p[1], p[3], p[5]])

# Ciclo for
# <forLoop> -> for <id> := <expression> to <expression> do <instruction>
def p_for(p):
    """for : TkFor TkId TkAsig expression TkTo expression TkDo instruction"""
    p[0] = AST("For", [p[2], p[4], p[6], p[8]], [p[1], p[3], p[5], p[7]])

# Ciclo do
# <doLoop> -> do <instruction> while <expression>
def p_do(p):
    """do : TkDo instruction"""
    p[0] = AST("Do", [p[2], p[4]], [p[1], p[3]])

# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Error: Sintax error in row %d, column %d: unexpected token '%s'." % (
            p.lineno, p.lexpos, p.value))
    else:
        print("Error: Unexpected end of input")
