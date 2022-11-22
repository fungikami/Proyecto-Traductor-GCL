"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class AST:
    pass

# ------------------ BLOCK ------------------
class Block(AST):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs

    def imprimir(self, level):
        if (self.decls.seq_decls):
            return f'{"-" * level}Block\n{self.decls.imprimir(level + 1)}\n{self.instrs.imprimir(level + 1)}'
        else:
            return f'{"-" * level}Block\n{self.instrs.imprimir(level + 1)}'

# ------------------ DECLARATIONS ------------------
class Declare(AST):
    def __init__(self, seq_decls):
        self.seq_decls = seq_decls

    def imprimir(self, level):
        return f'{"-" * level}Declare\n{self.seq_decls.imprimir(level + 1)}'

class Declaration(AST):
    def __init__(self, idLists, type):
        self.idLists = idLists
        self.type = type

    def imprimir(self, level):
        return f'{"-" * level}{self.idLists} : {self.type}'

# ------------------ SEQUENCING ------------------
class Sequencing(AST):
    def __init__(self, instr1, instr2):
        self.instr1 = instr1
        self.instr2 = instr2

    def imprimir(self, level):
        return f'{"-" * level}Sequencing\n{self.instr1.imprimir(level + 1)}\n{self.instr2.imprimir(level + 1)}'

class IdLists(AST):
    def __init__(self, id, idLists):
        self.id = id
        self.idLists = idLists

    def __str__(self):
        if self.idLists:
            return f'{self.id}, {self.idLists}'
        return f'{self.id}'

    def imprimir(self, level):
        return f'{"-" * level}IdLists\n{self.id.imprimir(level + 1)}\n{self.idLists.imprimir(level + 1)}'

# ------------------ SKIP ------------------
class Skip(AST):
    def __init__(self):
        pass

    def imprimir(self, level):
        return f'{"-" * level}skip'

# ------------------ ASSIGMENT ------------------
class Asig(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}Asig\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class Comma(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Comma\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ BINARY OPERATORS ------------------
class Plus(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Plus\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Minus(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Minus\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Mult(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Mult\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class And(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}And\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Or(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Or\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Equal(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Equal\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class NEqual(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}NEqual\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Less(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Less\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Leq(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Leq\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Greater(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Greater\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Geq(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Geq\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ UNARY OPERATORS ------------------
class UnaryMinus(AST):
    def __init__(self, expr):
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}Minus\n{self.expr.imprimir(level + 1)}'

class Not(AST):
    def __init__(self, expr):
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}Not\n{self.expr.imprimir(level + 1)}'

# ------------------ ARRAYS ------------------
class ReadArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}ReadArray\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class WriteArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}WriteArray\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class TwoPoints(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}TwoPoints\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ PRINT ------------------
class Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def imprimir(self, level):
        return f'{"-" * level}Print\n{self.expr.imprimir(level + 1)}'

# ------------------ CONCAT ------------------
class Concat(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}Concat\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ IF ------------------
class If(AST):
    def __init__(self, guards):
        self.guards = guards

    def imprimir(self, level):
        return f'{"-" * level}If\n{self.guards.imprimir(level + 1)}'

class Guard(AST):
    def __init__(self, guards, guard):
        self.guards = guards
        self.guard = guard

    def imprimir(self, level):
        return f'{"-" * level}Guard\n{self.guards.imprimir(level + 1)}\n{self.guard.imprimir(level + 1)}'

class Then(AST):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts

    def imprimir(self, level):
        return f'{"-" * level}Then\n{self.expr.imprimir(level + 1)}\n{self.stmts.imprimir(level + 1)}'

# ------------------ FOR LOOP ------------------
class For(AST):
    def __init__(self, range, instr):
        self.range = range
        self.instr = instr

    def imprimir(self, level):
        return f'{"-" * level}For\n{self.range.imprimir(level + 1)}\n{self.instr.imprimir(level + 1)}'

class In(AST):
    def __init__(self, id, range):
        self.id = id
        self.range = range

    def imprimir(self, level):
        return f'{"-" * level}In\n{self.id.imprimir(level + 1)}\n{self.range.imprimir(level + 1)}'

class To(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def imprimir(self, level):
        return f'{"-" * level}To\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ DO LOOP ------------------
class Do(AST):
    def __init__(self, stmts):
        self.stmts = stmts

    def imprimir(self, level):
        return f'{"-" * level}Do\n{self.stmts.imprimir(level + 1)}'

# ------------------ TYPES ------------------
class Type(AST):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f'{self.type}'

    # def imprimir(self, level):
    #     return f'{"-" * level}Type\n{self.type}'

class ArrayType(AST):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'array[{self.start}..{self.end}]'

    def imprimir(self, level):
        print("-" * level + "ArrayType")
        self.start.imprimir(level + 1)
        self.end.imprimir(level + 1)

# ------------------ TERMINALS ------------------
class Id(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def imprimir(self, level):
        return f'{"-" * level}Ident: {self.value}'

class Number(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Literal: {self.value}'

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value}'

class Boolean(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value}'

class String(AST):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def imprimir(self, level):
        return f'{"-" * level}String: "{self.value}"'
