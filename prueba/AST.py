"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class AST:
    pass

# Block: Imprime -Block
class Block(AST):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs

    def imprimir(self, level):
        print("-" * level + "Block")
        if self.decls:
            self.decls.imprimir(level + 1)
        if self.instrs:
            self.instrs.imprimir(level + 1)

# Declaraciones: Imprime -Declare
class Declare(AST):
    def __init__(self, seq_decls):
        self.seq_decls = seq_decls

    def imprimir(self, level):
        print("-" * level + "Declare")
        self.seq_decls.imprimir(level + 1)

# Secuencias: Imprime -Sequencing
class Sequencing(AST):
    def __init__(self, instr1, instr2):
        self.instr1 = instr1
        self.instr2 = instr2

    def imprimir(self, level):
        print("-" * level + "Sequencing")
        self.instr1.imprimir(level + 1)
        self.instr2.imprimir(level + 1)

class Declaration(AST):
    def __init__(self, idLists, type):
        self.idLists = idLists
        self.type = type

    def imprimir(self, level):
        self.idLists.imprimir(level + 1)
        self.type.imprimir(level + 1)

class IdLists(AST):
    def __init__(self, id, idLists):
        self.id = id
        self.idLists = idLists

    def imprimir(self, level):
        print("-" * level + "IdLists")
        self.idLists.imprimir(level + 1)

class Asig(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        print("-" * level + "Asig")
        self.id.imprimir(level + 1)
        self.expr.imprimir(level + 1)


# Operaciones
class Plus(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Plus")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Minus(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Minus")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Mult(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Mult")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class And(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "And")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Or(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Or")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Equal(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Equal")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class NEqual(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "NEqual")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Less(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Less")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Leq(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Leq")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Greater(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Greater")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Geq(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Geq")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

# Arreglos
class WriteArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        print("-" * level + "WriteArray")
        self.id.imprimir(level + 1)
        self.expr.imprimir(level + 1)

class ReadArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        print("-" * level + "ReadArray")
        self.id.imprimir(level + 1)
        self.expr.imprimir(level + 1)

# Salida
class Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def imprimir(self, level):
        print("-" * level + "Print")
        self.expr.imprimir(level + 1)

class Concatenation(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        print("-" * level + "Concat")
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)

class Conditional(AST):
    def __init__(self, guards):
        self.guards = guards

    def imprimir(self, level):
        print("-" * level + "If")
        self.guards.imprimir(level + 1)

class Guards(AST):
    def __init__(self, guard, guards):
        self.guard = guard
        self.guards = guards

    def imprimir(self, level):
        print("-" * level + "Guard")
        self.guard.imprimir(level + 1)
        self.guards.imprimir(level + 1)

class Guard(AST):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts

    def imprimir(self, level):
        print("-" * level + "Then")
        self.expr.imprimir(level + 1)
        self.stmts.imprimir(level + 1)

class For(AST):
    def __init__(self, id, expr1, expr2, stmts):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        self.stmts = stmts

    def imprimir(self, level):
        print("-" * level + "For")
        self.id.imprimir(level + 1)
        self.expr1.imprimir(level + 1)
        self.expr2.imprimir(level + 1)
        self.stmts.imprimir(level + 1)

class Do(AST):
    def __init__(self, stmts, expr):
        self.stmts = stmts
        self.expr = expr

    def imprimir(self, level):
        print("-" * level + "Do")
        self.stmts.imprimir(level + 1)
        self.expr.imprimir(level + 1)

# Tipos
class Type(AST):
    def __init__(self, type):
        self.type = type

    def imprimir(self, level):
        print("-" * level + "Type")
        print("-" * (level + 1) + self.type)

class ArrayType(AST):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def imprimir(self, level):
        print("-" * level + "ArrayType")
        self.start.imprimir(level + 1)
        self.end.imprimir(level + 1)

# Terminales
class Id(AST):
    def __init__(self, value):
        self.value = value

    def imprimir(self, level):
        print("-" * level + "Ident: " + self.value)

class Number(AST):
    def __init__(self, value):
        self.value = value
    
    def imprimir(self, level):
        print("-" * level + "Literal: " + str(self.value))

class Boolean(AST):
    def __init__(self, value):
        self.value = value

    def imprimir(self, level):
        print("-" * level + "Literal: " + str(self.value))

class String(AST):
    def __init__(self, value):
        self.value = value

    def imprimir(self, level):
        print("-" * level + "String: " + self.value)
