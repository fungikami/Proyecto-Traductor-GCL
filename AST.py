"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class AST:
    pass 


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
