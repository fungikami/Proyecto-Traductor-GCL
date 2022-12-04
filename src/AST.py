"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from SymbolTable import *
import sys

class AST:
    pass

class Program(AST):
    def __init__(self, block):
        self.block = block

        # Crea una pila de Tabla de Símbolos
        # Hay que tener una pila dado que podemos tener bloques anidados
        self.symTabStack = SymbolTable()

    def decorate(self):
        self.block.decorate(self.symTabStack)

    def imprimir(self, level):
        return self.block.imprimir(level)

# ------------------ BLOCK ------------------
class Block(AST):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs

        # Crea una nueva Tabla de Símbolos
        # self.symTab = SymbolTable()

    def decorate(self, symTabStack: SymbolTable):
        # Empila una nueva Tabla de Símbolos. 
        # MOSCA, pa revisar la lista debe ser de atrás para adelante
        symTabStack.open_scope()

        # Decorar la tabla de simbolos
        self.decls.decorate(symTabStack)
        self.instrs.decorate(symTabStack)

        # Desempila la Tabla de Símbolos
        symTabStack.close_scope()

    def imprimir(self, level):
        if (self.decls.seq_decls):
            return f'{"-" * level}Block\n{self.decls.imprimir(level + 1)}\n{self.instrs.imprimir(level + 1)}'
        else:
            return f'{"-" * level}Block\n{self.instrs.imprimir(level + 1)}'

# ------------------ DECLARATIONS ------------------
class Declare(AST):
    def __init__(self, seq_decls):
        self.seq_decls = seq_decls

    def decorate(self, symTabStack):
        if self.seq_decls:
            self.seq_decls.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Symbols Table\n{self.seq_decls.imprimir(level + 1, True)}'

class Declaration(AST):
    def __init__(self, idLists, type):
        self.idLists = idLists
        self.type = type

    def decorate(self, symTabStack):
        # ARREGLAR PARA QUE SE LOOPEA POR LA PILA   
        # Obtiene la Tabla de Símbolos del tope de la pila
        # symTab = symTabStack[-1]

        # Inserta cada id en la tabla de símbolos
        # OJO owo VER DONDE ATRAPAR EXCEPCIONES AaaaaaaaaaaaAa
        if ARRAY in self.type.name:
            tmp = self.type.name.split('..')
            if tmp[0][-1] > tmp[1][0]:
                raise Exception(f'Error: El rango del arreglo {self.type.name} es inválido')

        for id in self.idLists:
            symTabStack.insert(id.value, self.type.name, None)
            id.type = self.type.name

        # Si es un arreglo, hay que verificar que el end > start. Pero esta verif 
        # se hace es dinámica (no se hace por ahora, pero lo anota para recordarlo)

    def imprimir(self, level, isDecl = False):
        # Convierte la lista de id's en un string
        # idList = ', '.join([str(id) for id in self.idLists])
        result = ''
        for id in self.idLists:
            result += f'{"-" * level}variable: {id.value} | type: {self.type.name}\n'
        return result.rstrip()

# ------------------ SEQUENCING ------------------
class Sequencing(AST):
    def __init__(self, instr1, instr2):
        self.instr1 = instr1
        self.instr2 = instr2

    def decorate(self, symTabStack):
        self.instr1.decorate(symTabStack)
        self.instr2.decorate(symTabStack)

    def imprimir(self, level, isDecl = False):
        if isDecl:
            return f'{self.instr1.imprimir(level)}\n{self.instr2.imprimir(level)}'
        return f'{"-" * level}Sequencing\n{self.instr1.imprimir(level + 1)}\n{self.instr2.imprimir(level + 1)}'

# class IdLists(AST):
#     def __init__(self, id, idLists):
#         self.id = id
#         self.idLists = idLists

#     def __str__(self):
#         if self.idLists:
#             return f'{self.id}, {self.idLists}'
#         return f'{self.id}'

#     # No se usa
#     # def imprimir(self, level):
#     #     return f'{"-" * level}IdLists\n{self.id.imprimir(level + 1)}\n{self.idLists.imprimir(level + 1)}'

# ------------------ SKIP ------------------
class Skip(AST):
    def __init__(self):
        pass

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}skip'

# ------------------ ASSIGMENT ------------------
class Asig(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def decorate(self, symTabStack):
        # Obtiene la Tabla de Símbolos del tope de la pila
        # symTab = symTabStack[-1]

        # Busca el id en la tabla de símbolos
        idType = symTabStack.get_type(self.id.value)

        # Decorar la expresión
        self.expr.decorate(symTabStack)

        # Verificar que el tamaño de los arreglos sea el mismo que el definido
        if idType.startswith(ARRAY) and self.expr.type.startswith(ARRAY):
            # Obtiene el tamaño del arreglo del definido en la tabla de símbolos 
            arrRange = idType.split('[')[1].split(']')[0].split('..')
            expectedLength = int(arrRange[1]) - int(arrRange[0]) + 1

            # Obtiene el tamaño del arreglo del tipo de la expresión
            arrLength = int(self.expr.type.split('=')[1])

            if expectedLength != arrLength:
                raise Exception(f'Error: El tamaño del arreglo no coincide con el definido')
            
        else:
            if idType != self.expr.type:
                raise Exception(f'Error: El tipo de la expresión no coincide con el tipo del id')

        symTabStack.update(self.id.value, self.expr.value)
        # # Decorar el id
        self.id.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Asig\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class Comma(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.len = 1 + self.expr1.len if isinstance(self.expr1, Comma) else 2
        self.type = f'{ARRAY} with length={self.len}'
        self.value = f'{self.expr1.value}, {self.expr2.value}'

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        if not isinstance(self.expr1, Comma) and self.expr1.type != INT:
            raise Exception(f'Error: El tipo de la expresión no es int. Expresión: {self.expr1.type}')

        self.expr2.decorate(symTabStack)
        if self.expr2.type != INT:
            raise Exception(f'Error: El tipo de la expresión no es int. Expresión: {self.expr2.type}')
      

    def imprimir(self, level):
        return f'{"-" * level}Comma | type: {self.type}\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ BINARY OPERATORS ------------------
class BinOp(AST):
    def __init__(self, expr1, expr2, expectedType, valueType):
        self.expr1 = expr1
        self.expr2 = expr2
        self.expectedType = expectedType
        self.type = valueType
        # self.value = f'{self.expr1.value} + {self.expr2.value}'

    def decorate(self, symTabStack):
        # Caso para el == y != que pueden comparar booleanos o enteros
        if self.expectedType == ANY:
            self.expr1.decorate(symTabStack)
            self.expr2.decorate(symTabStack)

            # Verifica que los tipos de las expresiones sean iguales
            if self.expr1.type != self.expr2.type:
                raise Exception(f'Error: Los tipos de las expresiones no coinciden.')

        else:
            self.expr1.decorate(symTabStack)
            if (self.expr1.type != self.expectedType):
                raise Exception(f'Error: El tipo de la expresión esperado es {self.expectedType}, pero se obtuvo {self.expr1.type}')

            self.expr2.decorate(symTabStack)
            if (self.expr2.type != self.expectedType):
                raise Exception(f'Error: El tipo de la expresión esperado es {self.expectedType}, pero se obtuvo {self.expr2.type}')

class Plus(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, INT)
        self.value = f'{self.expr1.value} + {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Plus\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Minus(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, INT)
        self.value = f'{self.expr1.value} - {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Minus\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Mult(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, INT)
        self.value = f'{self.expr1.value} * {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Mult\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class And(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, BOOL, BOOL)
        self.value = f'{self.expr1.value} /\ {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}And\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Or(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, BOOL, BOOL)
        self.value = f'{self.expr1.value} \/ {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Or\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Equal(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, ANY, BOOL)
        self.value = f'{self.expr1.value} == {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Equal\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class NEqual(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, ANY, BOOL)
        self.value = f'{self.expr1.value} != {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}NotEqual\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Less(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, BOOL)
        self.value = f'{self.expr1.value} < {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Less\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Leq(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, BOOL)
        self.value = f'{self.expr1.value} <= {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Leq\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Greater(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, BOOL)
        self.value = f'{self.expr1.value} > {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Greater\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Geq(BinOp):
    def __init__(self, expr1, expr2):
        super().__init__(expr1, expr2, INT, BOOL)
        self.value = f'{self.expr1.value} >= {self.expr2.value}'

    def imprimir(self, level):
        return f'{"-" * level}Geq\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ UNARY OPERATORS ------------------
class UnaryMinus(AST):
    def __init__(self, expr):
        self.expr = expr
        self.type = INT
        self.value = f'-{self.expr.value}'

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        if self.expr.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.expr.type}')

    def __str__(self):
        return f'-{self.expr}'

    def imprimir(self, level):
        return f'{"-" * level}Minus\n{self.expr.imprimir(level + 1)}'

class Not(AST):
    def __init__(self, expr):
        self.expr = expr
        self.type = BOOL
        self.value = f'!{self.expr.value}'

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        if self.expr.type != BOOL:
            raise Exception(f'Error: El tipo de la expresión esperado es {BOOL}, pero se obtuvo {self.expr.type}')

    def imprimir(self, level):
        return f'{"-" * level}Not\n{self.expr.imprimir(level + 1)}'

# ------------------ ARRAYS ------------------
class ReadArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        # Como solo hay arreglos de enteros leer un arreglo siempre deberia dar un entero
        self.type = INT
        self.value = f'{id}[{expr}]'

    def decorate(self, symTabStack):
        # symTab = symTabStack[-1]
        value = symTabStack.get_value(self.id.value) 
        if value is None:
            raise Exception(f'Error: El arreglo {self.id.value} no ha sido inicializado')

        # Decorar id
        self.id.decorate(symTabStack)

        self.expr.decorate(symTabStack)
        if self.expr.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.expr.type}')
        # No se si deberiamos verificar que el valor de expr este en el rango del arreglo
        # self.type = symTabStack[-1].get_type(self.id.value)

    def imprimir(self, level):
        return f'{"-" * level}ReadArray\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class WriteArray(AST):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
        self.value = f'{id}({expr.value})'

    def decorate(self, symTabStack):
        if isinstance(self.id, Id):
            value = symTabStack.get_value(self.id.value) 
            if value is None:
                raise Exception(f'Error: El arreglo {self.id.value} no ha sido inicializado')
        self.id.decorate(symTabStack)
        self.expr.decorate(symTabStack)
        if self.expr.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.expr.type}')

        # Ver como agregar los elementos al arreglo en la tabla de símbolos
        #symTabStack.update(self.id, self.expr.type)

    def imprimir(self, level):
        return f'{"-" * level}WriteArray\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class TwoPoints(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.value = f'{expr1}:{expr2}'

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        self.expr2.decorate(symTabStack)
        if self.expr1.type != INT or self.expr2.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.expr1.type} y {self.expr2.type}')

    def imprimir(self, level):
        return f'{"-" * level}TwoPoints\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ PRINT ------------------
class Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Print\n{self.expr.imprimir(level + 1)}'

# ------------------ CONCAT ------------------
class Concat(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2
        self.type = STR

    def decorate(self, symTabStack):
        # REVISAR SI HAY QUE VERIFICAR ALGO
        pass

    def imprimir(self, level):
        return f'{"-" * level}Concat\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ IF ------------------
class If(AST):
    def __init__(self, guards):
        self.guards = guards

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}If\n{self.guards.imprimir(level + 1)}'

class Guard(AST):
    def __init__(self, guards, guard):
        self.guards = guards
        self.guard = guard

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)
        self.guard.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Guard\n{self.guards.imprimir(level + 1)}\n{self.guard.imprimir(level + 1)}'

class Then(AST):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        self.stmts.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Then\n{self.expr.imprimir(level + 1)}\n{self.stmts.imprimir(level + 1)}'

# ------------------ FOR LOOP ------------------
class For(AST):
    def __init__(self, range, instr):
        self.range = range
        self.instr = instr

    def decorate(self, symTabStack):
        self.range.decorate(symTabStack)
        self.instr.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}For\n{self.range.imprimir(level + 1)}\n{self.instr.imprimir(level + 1)}'

class In(AST):
    def __init__(self, id, range):
        self.id = id
        self.range = range

    def decorate(self, symTabStack):
        self.range.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}In\n{self.id.imprimir(level + 1)}\n{self.range.imprimir(level + 1)}'

class To(AST):
    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        self.expr2.decorate(symTabStack)
        if self.expr1.type != INT or self.expr2.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.expr1.type} y {self.expr2.type}')

    def imprimir(self, level):
        return f'{"-" * level}To\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ DO LOOP ------------------
class Do(AST):
    def __init__(self, stmts):
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.stmts.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Do\n{self.stmts.imprimir(level + 1)}'

# ------------------ TYPES ------------------
class Type(AST):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def decorate(self, symTabStack):
        pass

    # def imprimir(self, level):
    #     return f'{"-" * level}Type\n{self.type}'

class ArrayType(AST):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = f'{ARRAY}[{self.start}..{self.end}]'

    def __str__(self):
        return f'array[Literal: {self.start}..Literal: {self.end}]'

    def decorate(self, symTabStack):
        self.start.decorate(symTabStack)
        if self.start.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.start.type}')

        self.end.decorate(symTabStack)
        if self.end.type != INT:
            raise Exception(f'Error: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.end.type}')

    def imprimir(self, level):
        print("-" * level + "ArrayType")
        self.start.imprimir(level + 1)
        self.end.imprimir(level + 1)

# ------------------ TERMINALS ------------------
class Id(AST):
    def __init__(self, value):
        self.value = value
        self.type = None
        self.idValue = None

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        # Obtener el tope de la pila de tablas de símbolos
        self.type = symTabStack.get_type(self.value)

        self.idValue = symTabStack.get_value(self.value)
        if self.idValue == None:
            raise Exception(f'Error: El identificador \'{self.value}\' no esta inicializado')


    def imprimir(self, level):
        return f'{"-" * level}Ident: {self.value} | type: {self.type}'

class Number(AST):
    def __init__(self, value):
        self.value = value
        self.type = INT

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

class Boolean(AST):
    def __init__(self, value):
        self.value = value
        self.type = BOOL

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

class String(AST):
    def __init__(self, value):
        self.value = value
        self.type = STR

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}String: "{self.value}"'


# Alias para tipos de datos
INT = 'int'
BOOL = 'bool'
STR = 'str'
ARRAY = 'array'

# ANY es que puede ser entero o booleano
ANY = 'any'