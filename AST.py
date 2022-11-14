"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class AST:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def __str__(self) -> str:
        if isinstance(self.children, AST):
            if self.leaf:
                return f"AST:= {self.type}(`{self.leaf}`, {self.children})"
            else:
                return f"AST:= {self.type}({self.children})"
        if isinstance(self.children, list):
            if self.children and self.leaf:
                if len(self.children) == 2:
                    return f"(AST:= {self.type} L:{self.children[0]} R:{self.children[1]} `{self.leaf}`)"
                else:
                    return f"(AST:= {self.type} L:{self.children[0]} R:None `{self.leaf}`)"
            elif self.children:
                if len(self.children) == 2:
                    return f"(AST:= {self.type} L:{self.children[0]} R:{self.children[1]} NoLeaf)"
                else:
                    return f"(AST:= {self.type} L:{self.children[0]} R:None NoLeaf)"
        elif self.leaf:
            return f"(AST:= {self.type} NoChildren `{self.leaf}`)"
        else:
            return f"(AST:= {self.type} NoChildren NoLeaf)"

    def __repr__(self) -> str:
        return self.__str__()

# class Program(AST):
#     def __init__(self, block):
#         AST.__init__(self, "Program", [block])

# # Block: Declare, Sequencing
# class Block(AST):
#     def __init__(self, decls, instrs):
#         AST.__init__(self, "Block", [decls, instrs])

# class Declarations(AST):
#     def __init__(self, declaration, seq_decls):
#         AST.__init__(self, "Declarations", [declaration, seq_decls])

# class Declare(AST):
#     def __init__(self, seq_decls):
#         AST.__init__(self, "Declare", [seq_decls])

# class Sequencing(AST):
#     def __init__(self, instr1, instr2):
#         self.instr1 = instr1
#         self.instr2 = instr2

# class Declaration(AST):
#     def __init__(self, idLists, type):
#         self.idLists = idLists
#         self.type = type

# class List(AST):
#     def __init__(self, id, idLists):
#         self.idLists = idLists
#         self.id = id

# class Asig(AST):
#     def __init__(self, id, expr):
#         self.id = id
#         self.expr = expr



# # Terminales
# class Terminal(AST):
#     def __init__(self, type, value):
#         AST.__init__(self, type)
#         self.value = value

# class Number(Terminal):
#     def __init__(self, value):
#         Terminal.__init__(self, 'TkNumber', value)

# class String(Terminal):
#     def __init__(self, value):
#         Terminal.__init__(self, 'TkString', value)

# class Id(Terminal):
#     pass

# class Boolean(Terminal):
#     def __init__(self, value):
#         Terminal.__init__(self, 'TkBoolean', value)

# # Tipos
# class Type(AST):
#     pass

# # Operaciones binarias
# class BinOp(AST):
#     pass

# # Operaciones unarias
# class UnOp(AST):
#     pass

# # Otros
