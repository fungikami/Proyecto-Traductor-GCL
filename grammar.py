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
# Programa es un bloque
def p_program(p):
    """program : block"""

# Bloque, puede ir Declaración y Secuenciación (Preguntar si es válido un bloque vacío)
def p_block(p):
    """block : TkOBlock TkCBlock
             | TkOBlock declaration TkCBlock
             | TkOBlock declaration sequence TkCBlock
    """

# Declaraciones, puede ir una secuencia de declaraciones
def p_declarations(p):
    """declarations : declare seq_declarations
                    | declare seq_declarations TkSemicolon declarations
    """

# Secuencia de declaraciones, puede ir una secuencia de declaraciones
def p_seq_declarations(p):
    """seq_declarations : declaration
                        | seq_declarations TkSemicolon declaration
    """

# Declaración, como a, b, i : int
def p_declaration(p):

# Asignación, como a := 1 + a
def p_asignation(p):
    """asignation : TkId TkAsig expression"""

# Expresión, como a + b o a v b
def p_expression(p):
    """expression : expression TkPlus expression
                    | expression TkMinus expression
                    | expression TkMult expression
                    | expression TkOr expression
                    | expression TkAnd expression
                    | expression TkEqual expression
                    | expression TkNEqual expression
                    | expression TkLess expression
                    | expression TkLeq expression
                    | expression TkGeq expression
                    | expression TkGreater expression
                    | TkOpenPar expression TkClosePar
                    | TkNot expression
                    | TkId
                    | TkNumber
                    | TkTrue
                    | TkFalse
                    | array
                    | arrayAccess
        """

    

# Error: Sintax error in row 2, column 10: unexpected token ’;’.
def p_error(p):
    if p:
        print("Error: Sintax error in row %d, column %d: unexpected token '%s'." % (p.lineno, p.lexpos, p.value))
    else:
        print("Error: Unexpected end of input")


def p_for(p):
    """for : TkFor TkId TkIn expression TkDo block TkEnd"""

