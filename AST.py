"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class AST:
    pass 

# Block: Declare, Sequencing
class Block(AST):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs

class Declare(AST):
    def __init__(self, instr):
        pass

class Sequencing(AST):
    def __init(self, instr1, instr2):
        self.instr1 = instr1
        self.instr2 = instr2

class Declaration(AST):
    def __init__(self, idLists, type):
        self.idLists = idLists
        self.type = type

class List(AST):
    def __init__(self, id, idLists):
        self.idLists = idLists
        self.id = id

class Asig(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr



# Terminales
class Terminal(AST):
    pass 

class Number(Terminal):
    pass 

class String(Terminal):
    pass

class Id(Terminal):
    pass

class Boolean(Terminal):
    pass

# Tipos
class Type(AST):
    pass

# Operaciones binarias
class BinOp(AST):
    pass

# Operaciones unarias
class UnOp(AST):
    pass

# Otros
