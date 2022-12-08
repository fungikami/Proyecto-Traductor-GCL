"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from SymbolTable import *
import sys

class AST:
    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column

class Program(AST):
    def __init__(self, block, row, column) -> None:
        super().__init__(row, column)
        self.block = block

        # Crea una Tabla de Símbolos
        self.symTabStack = SymbolTable()

    def decorate(self):
        self.block.decorate(self.symTabStack)

    def imprimir(self, level):
        return self.block.imprimir(level)

# ------------------ BLOCK ------------------
class Block(AST):
    def __init__(self, decls, instrs, row, column) -> None:
        super().__init__(row, column)
        self.decls = decls
        self.instrs = instrs

    def decorate(self, symTabStack: SymbolTable):
        # Empila una nueva Tabla de Símbolos. 
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
    def __init__(self, seq_decls, row, column) -> None:
        super().__init__(row, column)
        self.seq_decls = seq_decls

    def decorate(self, symTabStack):
        if self.seq_decls:
            self.seq_decls.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Symbols Table\n{self.seq_decls.imprimir(level + 1, True)}'

class Declaration(AST):
    def __init__(self, idLists, type, row, column) -> None:
        super().__init__(row, column)
        self.idLists = idLists
        self.type = type

    def decorate(self, symTabStack):
        # Si es un arreglo, verifica que el tamaño sea > 0
        if ARRAY in self.type.name:
            tmp = self.type.name.split('..')
            if tmp[0][-1] > tmp[1][0]:
                raise Exception(f'Error in row {self.row}, column {self.column}: {self.type.name} does not have a valid size')

        # Inserta cada id en la tabla de símbolos
        for id in self.idLists:
            symTabStack.insert(id.value, self.type.name, None, self.row, self.column)
            id.type = self.type.name

    def imprimir(self, level, isDecl = False):
        # Convierte la lista de id's en un string
        # idList = ', '.join([str(id) for id in self.idLists])
        result = ''
        for id in self.idLists:
            result += f'{"-" * level}variable: {id.value} | type: {self.type.name}\n'
        return result.rstrip()

# ------------------ SEQUENCING ------------------
class Sequencing(AST):
    def __init__(self, instr1, instr2, row, column) -> None:
        super().__init__(row, column)
        self.instr1 = instr1
        self.instr2 = instr2

    def decorate(self, symTabStack):
        self.instr1.decorate(symTabStack)
        self.instr2.decorate(symTabStack)

    def imprimir(self, level, isDecl = False):
        if isDecl:
            return f'{self.instr1.imprimir(level, True)}\n{self.instr2.imprimir(level, True)}'
        return f'{"-" * level}Sequencing\n{self.instr1.imprimir(level + 1)}\n{self.instr2.imprimir(level + 1)}'

# ------------------ SKIP ------------------
class Skip(AST):
    def __init__(self) -> None:
        pass
        
    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}skip'

# ------------------ ASSIGMENT ------------------
class Asig(AST):
    def __init__(self, id, expr, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.expr = expr

    def decorate(self, symTabStack):
        # Busca el tipo del id en la tabla de símbolos
        idType = symTabStack.get_type(self.id.value, self.row, self.column)

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
                raise Exception(f'Error in row {self.row}, column {self.column}: {self.id.value} does not have the same size defined in the declaration')
            
        else:
            if idType != self.expr.type:
                raise Exception(f'Error in row {self.row}, column {self.column}: {self.id.value} is not of type {self.expr.type}')

        # idType = symTabStack.lookup(self.id.value, )[2]
        is_readonly = symTabStack.is_readonly(self.id.value, self.row, self.column)
        if is_readonly:
            raise Exception(f'Error in row {self.row}, column {self.column}: It is changing the variable "{self.id.value}", which is a control variable of a \'for\' statement')

        symTabStack.update(self.id.value, self.expr.value, self.row, self.column)
        # Decorar el id
        self.id.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Asig\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class Comma(AST):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2
        self.len = 1 + self.expr1.len if isinstance(self.expr1, Comma) else 2
        self.type = f'{ARRAY} with length={self.len}'
        self.value = f'{self.expr1.value}, {self.expr2.value}'

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        if not isinstance(self.expr1, Comma) and self.expr1.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: {self.expr1.value} is not of type {INT}')

        self.expr2.decorate(symTabStack)
        if self.expr2.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: {self.expr2.value} is not of type {INT}')
      
    def imprimir(self, level):
        return f'{"-" * level}Comma | type: {self.type}\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ BINARY OPERATORS ------------------
class BinOp(AST):
    def __init__(self, expr1, expr2, name, expectedType, valueType, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2
        self.name = name
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
                raise Exception(f'Error in row {self.row}, column {self.column}: {self.expr1.value} and {self.expr2.value} are not of the same type')

        else:
            self.expr1.decorate(symTabStack)
            if (self.expr1.type != self.expectedType):
                raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr1.value} is {self.expectedType} but is {self.expr1.type}')

            self.expr2.decorate(symTabStack)
            if (self.expr2.type != self.expectedType):
                raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr2.value} is {self.expectedType} but is {self.expr2.type}')

    def imprimir(self, level):
        return f'{"-" * level}{self.name} | type: {self.type}\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

class Plus(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Plus', INT, INT, row, column)
        self.value = f'{self.expr1.value} + {self.expr2.value}'

class Minus(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Minus', INT, INT, row, column)
        self.value = f'{self.expr1.value} - {self.expr2.value}'

class Mult(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Mult', INT, INT, row, column)
        self.value = f'{self.expr1.value} * {self.expr2.value}'

class And(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'And', BOOL, BOOL, row, column)
        self.value = f'{self.expr1.value} /\ {self.expr2.value}'

class Or(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Or', BOOL, BOOL, row, column)
        self.value = f'{self.expr1.value} \/ {self.expr2.value}'

class Equal(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Equal', ANY, BOOL, row, column)
        self.value = f'{self.expr1.value} == {self.expr2.value}'

class NEqual(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'NotEqual', ANY, BOOL, row, column)
        self.value = f'{self.expr1.value} != {self.expr2.value}'

class Less(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Less', INT, BOOL, row, column)
        self.value = f'{self.expr1.value} < {self.expr2.value}'

class Leq(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Leq', INT, BOOL, row, column)
        self.value = f'{self.expr1.value} <= {self.expr2.value}'

class Greater(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Greater', INT, BOOL, row, column)
        self.value = f'{self.expr1.value} > {self.expr2.value}'

class Geq(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Geq', INT, BOOL, row, column)
        self.value = f'{self.expr1.value} >= {self.expr2.value}'

# ------------------ UNARY OPERATORS ------------------
class UnaryMinus(AST):
    def __init__(self, expr, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr
        self.type = INT
        self.value = f'-{self.expr.value}'

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        if self.expr.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr.value} is {INT} but is {self.expr.type}')

    def __str__(self):
        return f'-{self.expr}'

    def imprimir(self, level):
        return f'{"-" * level}Minus | type: {self.type}\n{self.expr.imprimir(level + 1)}'

class Not(AST):
    def __init__(self, expr, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr
        self.type = BOOL
        self.value = f'!{self.expr.value}'

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        if self.expr.type != BOOL:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr.value} is {BOOL} but is {self.expr.type}')

    def imprimir(self, level):
        return f'{"-" * level}Not | type: {self.type}\n{self.expr.imprimir(level + 1)}'

# ------------------ ARRAYS ------------------
class ReadArray(AST):
    def __init__(self, id, expr, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.expr = expr
        # Como solo hay arreglos de enteros leer un arreglo siempre deberia dar un entero
        self.type = INT
        self.value = f'{id}[{expr}]'

    def decorate(self, symTabStack):
        value = symTabStack.get_value(self.id.value, self.row, self.column) 
        # if value is None:
        #     raise Exception(f'Error in row {self.row}, column {self.column}: Array {self.id.value} not initialized')

        # Decorar id
        self.id.decorate(symTabStack)

        self.expr.decorate(symTabStack)
        if self.expr.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr.value} is {INT} but is {self.expr.type}')
        
        # Verificar que el valor de expr este en el rango del arreglo

    def imprimir(self, level):
        return f'{"-" * level}ReadArray | type: {self.type}\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class WriteArray(AST):
    def __init__(self, id, expr, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.expr = expr
        self.value = f'{id}({expr.value})'

    def decorate(self, symTabStack):
        # if isinstance(self.id, Id):
        #     value = symTabStack.get_value(self.id.value) 
        #     if value is None:
        #         raise Exception(f'Error in row {self.row}, column {self.column}: Array {self.id.value} not initialized')
        
        self.id.decorate(symTabStack)
        self.expr.decorate(symTabStack)

        if self.expr.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr.value} is {INT} but is {self.expr.type}')

    def imprimir(self, level):
        return f'{"-" * level}WriteArray\n{self.id.imprimir(level + 1)}\n{self.expr.imprimir(level + 1)}'

class TwoPoints(AST):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2
        self.value = f'{expr1}:{expr2}'

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        self.expr2.decorate(symTabStack)
        if self.expr1.type != INT or self.expr2.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr1.value} and {self.expr2.value} is {INT} but is {self.expr1.type} and {self.expr2.type}')

    def imprimir(self, level):
        return f'{"-" * level}TwoPoints\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ PRINT ------------------
class Print(AST):
    def __init__(self, expr, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Print\n{self.expr.imprimir(level + 1)}'

# ------------------ CONCAT ------------------
class Concat(AST):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2
        self.type = STR

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        self.expr2.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Concat\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ IF ------------------
class If(AST):
    def __init__(self, guards, row, column) -> None:
        super().__init__(row, column)
        self.guards = guards

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}If\n{self.guards.imprimir(level + 1)}'

class Guard(AST):
    def __init__(self, guards, guard, row, column) -> None:
        super().__init__(row, column)
        self.guards = guards
        self.guard = guard

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)
        self.guard.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Guard\n{self.guards.imprimir(level + 1)}\n{self.guard.imprimir(level + 1)}'

class Then(AST):
    def __init__(self, expr, stmts, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        self.stmts.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Then\n{self.expr.imprimir(level + 1)}\n{self.stmts.imprimir(level + 1)}'

# ------------------ FOR LOOP ------------------
class For(AST):
    def __init__(self, range, instr, row, column) -> None:
        super().__init__(row, column)
        self.range = range
        self.instr = instr

    def decorate(self, symTabStack):
        symTabStack.open_scope()
        self.range.decorate(symTabStack)
        self.instr.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}For\n{self.range.imprimir(level + 1)}\n{self.instr.imprimir(level + 1)}'

class In(AST):
    def __init__(self, id, range, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.range = range

    def decorate(self, symTabStack):
        symTabStack.insert(self.id.value, INT, self.range.expr1.value, self.row, self.column, True)
        self.id.decorate(symTabStack)
        self.range.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}In\n{self.id.imprimir(level + 1)}\n{self.range.imprimir(level + 1)}'

class To(AST):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2

    def decorate(self, symTabStack):
        self.expr1.decorate(symTabStack)
        self.expr2.decorate(symTabStack)
        if self.expr1.type != INT or self.expr2.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: type expected for {self.expr1.value} and {self.expr2.value} is {INT} but is {self.expr1.type} and {self.expr2.type}')

    def imprimir(self, level):
        return f'{"-" * level}To\n{self.expr1.imprimir(level + 1)}\n{self.expr2.imprimir(level + 1)}'

# ------------------ DO LOOP ------------------
class Do(AST):
    def __init__(self, stmts, row, column) -> None:
        super().__init__(row, column)
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.stmts.decorate(symTabStack)

    def imprimir(self, level):
        return f'{"-" * level}Do\n{self.stmts.imprimir(level + 1)}'

# ------------------ TYPES ------------------
class Type(AST):
    def __init__(self, name, row, column) -> None:
        super().__init__(row, column)
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def decorate(self, symTabStack):
        pass

    # def imprimir(self, level):
    #     return f'{"-" * level}Type\n{self.type}'

class ArrayType(AST):
    def __init__(self, start, end, row, column) -> None:
        super().__init__(row, column)
        self.start = start
        self.end = end
        self.name = f'{ARRAY}[{self.start}..{self.end}]'

    def __str__(self):
        return f'array[Literal: {self.start}..Literal: {self.end}]'

    def decorate(self, symTabStack):
        self.start.decorate(symTabStack)
        if self.start.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.start.type}')

        self.end.decorate(symTabStack)
        if self.end.type != INT:
            raise Exception(f'Error in row {self.row}, column {self.column}: El tipo de la expresión esperado es {INT}, pero se obtuvo {self.end.type}')

    # def imprimir(self, level):
    #     print("-" * level + "ArrayType")
    #     self.start.imprimir(level + 1)
    #     self.end.imprimir(level + 1)

# ------------------ TERMINALS ------------------
class Id(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = None
        self.idValue = None

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        self.type = symTabStack.get_type(self.value, self.row, self.column)

        self.idValue = symTabStack.get_value(self.value, self.row, self.column)
        
        # if self.idValue == None:
        #     raise Exception(f'Error in row {self.row}, column {self.column}: Variable {self.value} not initialized')

    def imprimir(self, level):
        return f'{"-" * level}Ident: {self.value} | type: {self.type}'

class Number(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = INT

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

class Boolean(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = BOOL

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def imprimir(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

class String(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
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
ANY = 'any'     # ANY es que puede ser entero o booleano
