"""
    Árbol de Sintaxis Abstracta (AST) para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from SymbolTable import *
from PreAppTable import *
from utilities import *
import sys

N = 1

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

        # Para guardar espacios de estados, es de la forma:
        # [{x: [Tipo1, dummyVar1]}, {y: [Tipo2, dummyVar2]}}]
        self.preAppStack = []

        # Contador para los nombres de las variables dummy
        self.num = 0

    def decorate(self):
        self.block.decorate(self.symTabStack)

    def printAST(self, level):
        return self.block.printAST(level)

    def printPreApp(self, parser, lexer, esp=None):
        global par, lex, gesp
        par = parser
        lex = lexer
        gesp = esp
        return self.block.printPreApp(self.preAppStack)

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

    def printAST(self, level):
        if (self.decls.seq_decls):
            return f'{"-" * level}Block\n{self.decls.printAST(level + 1)}\n{self.instrs.printAST(level + 1)}'
        else:
            return f'{"-" * level}Block\n{self.instrs.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        # Agrega nuevo diccionario a la lista de espacios de estados
        esp.append({})
        
        # Declaraciones agregan los espacios de estados al diccionario nuevo
        self.decls.printPreApp(esp)

        # Compone los pi's con la sem[S]
        if len(esp[0]) == 0:
            toReturn = self.instrs.printPreApp(gesp, self.instrs.printPreApp(gesp))
        else:
            toReturn = composePi(esp, self.instrs.printPreApp(esp))

        # Desempila el diccionario
        esp.pop()

        return toReturn

# ------------------ DECLARATIONS ------------------
class Declare(AST):
    def __init__(self, seq_decls, row, column) -> None:
        super().__init__(row, column)
        self.seq_decls = seq_decls

    def decorate(self, symTabStack):
        if self.seq_decls:
            self.seq_decls.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}Symbols Table\n{self.seq_decls.printAST(level + 1, True)}'

    def printPreApp(self, esp, typ=None):
        if self.seq_decls:
            return self.seq_decls.printPreApp(esp, True)

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

    def printAST(self, level, isDecl = False):
        # Convierte la lista de id's en un string
        result = ''
        for id in self.idLists:
            result += f'{"-" * level}variable: {id.value} | type: {self.type.name}\n'
        return result.rstrip()

    def printPreApp(self, esp, typ=None, isDecl = False):
        global N
        # Agrega al ultimo diccionario de la lista los ids
        for id in self.idLists:
            esp[-1][id.value] = [getTypePreApp(self.type.name), f'x_{{{N}}}']
            N += 1

# ------------------ SEQUENCING ------------------
class Sequencing(AST):
    def __init__(self, instr1, instr2, row, column) -> None:
        super().__init__(row, column)
        self.instr1 = instr1
        self.instr2 = instr2

    def decorate(self, symTabStack):
        self.instr1.decorate(symTabStack)
        self.instr2.decorate(symTabStack)

    def printAST(self, level, isDecl = False):
        if isDecl:
            return f'{self.instr1.printAST(level, True)}\n{self.instr2.printAST(level, True)}'
        return f'{"-" * level}Sequencing\n{self.instr1.printAST(level + 1)}\n{self.instr2.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None, isDecl = False):
        # Si es una secuencia de declaraciones, se va por Declaration
        if isDecl:
            self.instr1.printPreApp(esp, True)
            self.instr2.printPreApp(esp, True)
            return

        # Composición de la sem de cada instrucción
        else:
            inst1 = self.instr1.printPreApp(esp)
            inst2 = self.instr2.printPreApp(esp)
            comp = f'({CIRC} {inst2} {inst1})'
            return comp

# ------------------ SKIP ------------------
class Skip(AST):
    def __init__(self, row, column) -> None:
        super().__init__(row, column)
        
    def decorate(self, symTabStack):
        pass

    def printAST(self, level):
        return f'{"-" * level}skip'

    def printPreApp(self, esp, typ=None):        
        # Retorna la función identidad con Esp'
        return identityFun(espPrima(esp))

# ------------------ ASSIGMENT ------------------
class Asig(AST):
    def __init__(self, id, expr, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.expr = expr
        self.value = f'{id.value} := {expr.value}'

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

    def printAST(self, level):
        return f'{"-" * level}Asig\n{self.id.printAST(level + 1)}\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        types = getListEsp(esp)                                 # [T1, T2, ..., Tn]
        range = crossProductRange(types)                        # (T1 x ... x Tn) x (T1 x ... x Tn)
        inRange = inRangePreApp('x_{120}', range)               # x in (T1 x ... x Tn) x (T1 x ... x Tn)
        
        vars = getListVar(esp)                                  # [x_1, x_2, ..., x_n]
        coord = coordenatesPreApp(vars)                         # (x_2, x_3)
        
        expr = self.expr.printPreApp(esp, self.id.type)         # x_1 + 89
        
        # POR ARREGLAR PARA QUE BUSQUE A PADRE SI NO ENCUENTRA EN SU BLOQUE
        dummyVar = esp[-1][self.id.value][1]                    # x_1 es la var dummy pa x
        
        sust = sustitution(vars, dummyVar, expr)                # [x + 89, x_3]
        sust = coordenatesPreApp(sust)                          # (x + 89, x_3) 
        
        tupl = tuplePreApp(coord, sust)                         # <(x_2, x_3), (x + 89, x_3)>
        equal = equalPreApp('x_{120}', tupl)                    # x = <(x_2, x_3), (x + 89, x_3)>

        anidateExist = anidateExistPreApp(vars, equal)          # E : | E : | < (x_2, x_3), (x + 89, x_3) >
        setAsig = setPreApp(inRange, anidateExist)              # { x in ... | E : | E : | < (x_2, x_3), (x + 89, x_3) > }
        setAbort = setPreApp(None, tuplePreApp(ABORT, ABORT))
        
        return f'({CUP} {setAbort} {setAsig})'

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

    def printAST(self, level):
        return f'{"-" * level}Comma | type: {self.type}\n{self.expr1.printAST(level + 1)}\n{self.expr2.printAST(level + 1)}'

    def getPreApp(self, esp, type):
        # Del tipo array[-1..1], obtiene el rango del arreglo
        # OJO con como está construido Comma, exp2 es el último elemento
        arrRange = type.split('[')[1].split(']')[0].split('..')
        arrSize = int(arrRange[1]) - int(arrRange[0]) + 1
        pos = int(arrRange[1]) - (arrSize - self.len)

        # Crea la tupla <pos, valor> de expr2
        exp2 = tuplePreApp(convertNumberPreApp(pos), self.expr2.printPreApp(esp, type))
        
        # Va recorriendo exp1 hasta llegar a un elemento que no sea Comma
        if (isinstance(self.expr1, Comma)):
            exp1 = self.expr1.getPreApp(esp, type)
        else:
            exp1 = tuplePreApp(convertNumberPreApp(pos-1), self.expr1.printPreApp(esp, type))

        return f'({COMMA} {exp2} {exp1})' 

    def printPreApp(self, esp, typ=None):       
        return setPreApp(None, self.getPreApp(esp, typ))

# ------------------ BINARY OPERATORS ------------------
class BinOp(AST):
    def __init__(self, expr1, expr2, name, expectedType, valueType, idPreApp, row, column) -> None:
        super().__init__(row, column)
        self.expr1 = expr1
        self.expr2 = expr2
        self.name = name
        self.expectedType = expectedType
        self.type = valueType
        # self.value = f'{self.expr1.value} + {self.expr2.value}'
        self.idPreApp = idPreApp

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

    def printAST(self, level):
        return f'{"-" * level}{self.name} | type: {self.type}\n{self.expr1.printAST(level + 1)}\n{self.expr2.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        exp1 = self.expr1.printPreApp(esp)
        exp2 = self.expr2.printPreApp(esp)
        return f'({self.idPreApp} {exp2} {exp1})'

class Plus(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Plus', INT, INT, PLUS, row, column)
        self.value = f'{self.expr1.value} + {self.expr2.value}'

class Minus(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Minus', INT, INT, MINUS, row, column)
        self.value = f'{self.expr1.value} - {self.expr2.value}'

class Mult(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Mult', INT, INT, TIMES, row, column)
        self.value = f'{self.expr1.value} * {self.expr2.value}'

class And(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'And', BOOL, BOOL, AND, row, column)
        self.value = f'{self.expr1.value} /\ {self.expr2.value}'

class Or(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Or', BOOL, BOOL, OR, row, column)
        self.value = f'{self.expr1.value} \/ {self.expr2.value}'

class Equal(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Equal', ANY, BOOL, EQUIV, row, column)
        self.value = f'{self.expr1.value} == {self.expr2.value}'

class NEqual(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'NotEqual', ANY, BOOL, NOTEQUIV, row, column)
        self.value = f'{self.expr1.value} != {self.expr2.value}'

class Less(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Less', INT, BOOL, LESS, row, column)
        self.value = f'{self.expr1.value} < {self.expr2.value}'

class Leq(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Leq', INT, BOOL, LEQ, row, column)
        self.value = f'{self.expr1.value} <= {self.expr2.value}'

class Greater(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Greater', INT, BOOL, GREATER, row, column)
        self.value = f'{self.expr1.value} > {self.expr2.value}'

class Geq(BinOp):
    def __init__(self, expr1, expr2, row, column) -> None:
        super().__init__(expr1, expr2, 'Geq', INT, BOOL, GEQ, row, column)
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

    def printAST(self, level):
        return f'{"-" * level}Minus | type: {self.type}\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'({UNARYMINUS} {self.expr.printPreApp()})'

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

    def printAST(self, level):
        return f'{"-" * level}Not | type: {self.type}\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'({NOT} {self.expr.printPreApp(esp)})'

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

    def printAST(self, level):
        return f'{"-" * level}ReadArray | type: {self.type}\n{self.id.printAST(level + 1)}\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

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

    def printAST(self, level):
        return f'{"-" * level}WriteArray\n{self.id.printAST(level + 1)}\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        exp1 = self.id.printPreApp()
        exp2 = self.expr.printPreApp()
        return f'({MODIFARRAY} {exp2} {exp1})'

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

    def printAST(self, level):
        return f'{"-" * level}TwoPoints\n{self.expr1.printAST(level + 1)}\n{self.expr2.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        exp1 = self.expr1.printPreApp()
        exp2 = self.expr2.printPreApp()
        return f'(({exp2}) ({exp1}))'

# ------------------ PRINT ------------------
class Print(AST):
    def __init__(self, expr, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}Print\n{self.expr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

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

    def printAST(self, level):
        return f'{"-" * level}Concat\n{self.expr1.printAST(level + 1)}\n{self.expr2.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

# ------------------ IF ------------------
class If(AST):
    def __init__(self, guards, row, column) -> None:
        super().__init__(row, column)
        self.guards = guards

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}If\n{self.guards.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        if isinstance(self.guards, Then):
            return self.guards.printPreApp(esp, isIf=True)
        return self.guards.printPreApp(esp)

class Guard(AST):
    def __init__(self, guards, guard, row, column) -> None:
        super().__init__(row, column)
        self.guards = guards
        self.guard = guard

    def decorate(self, symTabStack):
        self.guards.decorate(symTabStack)
        self.guard.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}Guard\n{self.guards.printAST(level + 1)}\n{self.guard.printAST(level + 1)}'
    
    def printPreApp(self, esp, typ=None):
        # Unión de las sem[<inst>] o id_ti
        instr = self.printSemInstr(esp)

        # Unión de los Ti
        cond = self.printSemCond(esp)

        # (U Ti)^C
        cond = f'({SUPERC} {cond})'

        # (U Ti)^C x abort
        abort = setPreApp(None, ABORT)
        condXAbort =f'({CROSSPROD} {abort} {cond})'

        # (U sem[<inst>] o id) U ((U Ti)^C x abort) 
        return f'({CUP} {condXAbort} {instr})'

    def printSemInstr(self, esp):
        guard = self.guard.printSemInstr(esp)
        guards = self.guards.printSemInstr(esp)
        return f'({CUP} {guard} {guards})'

    def printSemCond(self, esp):
        guard = self.guard.printSemCond(esp)
        guards = self.guards.printSemCond(esp)
        return f'({CUP} {guard} {guards})'

class Then(AST):
    def __init__(self, expr, stmts, row, column) -> None:
        super().__init__(row, column)
        self.expr = expr
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.expr.decorate(symTabStack)
        self.stmts.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}Then\n{self.expr.printAST(level + 1)}\n{self.stmts.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None, isIf=False):
        if isIf:
            # Unión de las sem[<inst>] o id_ti
            instr = self.printSemInstr(esp)

            # Unión de los Ti
            cond = self.printSemCond(esp)

            # (U Ti)^C
            cond = f'({SUPERC} {cond})'

            # (U Ti)^C x abort
            abort = setPreApp(None, ABORT)
            condXAbort =f'({CROSSPROD} {abort} {cond})'

            # (U sem[<inst>] o id) U ((U Ti)^C x abort) 
            return f'({CUP} {condXAbort} {instr})'
        return f'to-do' 

    def getSetCond(self, esp):
        ''' Retorna el conjunto Ti = {x in Exp | <condicion>} '''
        types = getListEsp(esp)                                 # [T1, T2, ..., Tn]
        range = crossProductRange(types)                        # (T1 x ... x Tn) x (T1 x ... x Tn)
        inRange = inRangePreApp('x_{120}', range)                    # x in (T1 x ... x Tn) x (T1 x ... x Tn)
        
        # POR ARREGLAR PARA QUE LA CONDICION NO TENGA LA VARIABLE DUMMY SINO LA GENERAL (x_{120})
        cond = self.expr.printPreApp(esp)                       # <condicion>
        setCond = setPreApp(inRange, cond)                      # {x in (T1 x ... x Tn) x (T1 x ... x Tn) | <condicion>}
        return setCond

    def getSemInstr(self, esp):
        ''' Retorna la sem[<instrucciones>] o id_ti '''
        idTi = identityFun(self.getSetCond(esp))
        toComp = [self.stmts.printPreApp(esp), idTi]
        comp = compose(toComp)
        return comp

    # ------------------------------ CASO IF ------------------------------
    def printSemInstr(self, esp):
        return self.getSemInstr(esp)

    def printSemCond(self, esp):
        ''' Retorna Ti '''
        return self.getSetCond(esp)

    # ---------------------------------------------------------------------

    # ------------------------------ CASO DO ------------------------------
    

# ------------------ DO LOOP ------------------
class Do(AST):
    def __init__(self, stmts, row, column) -> None:
        super().__init__(row, column)
        self.stmts = stmts

    def decorate(self, symTabStack):
        self.stmts.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}Do\n{self.stmts.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        # Letras fijas:
        C = 'x_{67}'
        D = 'x_{68}'
        i = 'x_{105}'
        m = 'x_{109}'
        x = 'x_{120}'
        y = 'x_{121}'
        z = 'x_{122}'

        # 1. Lado derecho del set
        espP = espPrima(esp)
        crossEspP = crossProductRange2(espP)            # Esp' x Esp'
        inRange = inRangePreApp(z, crossEspP)           # z in Esp' x Esp'

        # 2. Lado izquierdo del set
        Pesp = f'({PSET} {crossEspP})'                  # P(Esp'xEsp')
        inPesp = inRangePreApp(C, Pesp)                 # C in P(Esp'xEsp')

        # 3. (∀m|0 ≤ m ∧ m ≤ i : (m = 0 ∧ D(m) = sem[[Do0]]) ∨ (m > 0 ∧ D(m) = D(m − 1) ◦ sem[[If ]]))
        # (m = 0 ∧ D(m) = sem[[Do0 ]])
        semDo = f'({C})'                                                                    # ARREGLAR
        semDoStr = f'|[ if !({self.stmts.expr.value}) --> skip fi ]|'
        
        result = par.parse(semDoStr, lexer=lex)
        # result.decorate()
        semDo = result.printPreApp(par, lex, esp)

        dm = f'({CONCAT} ({D}) ({PAREN} {m}))'
        dm1 = binOpPreApp(EQUAL, dm, semDo) 
        body1 = binOpPreApp(AND, binOpPreApp(EQUAL, m, ZERO), dm1)

        # (m > 0 ∧ D(m) = D(m − 1) ◦ sem[[If ]])
        dm2 = binOpPreApp(EQUAL, dm, f'({CONCAT} ({D}) ({PAREN} ({MINUS} {ONE} {m})))') 
        body2 = binOpPreApp(AND, binOpPreApp(GREATER, m, ZERO), dm2)
        semIf = f'({C})'                                                                    # ARREGLAR 
        semIfStr = f'|[ if {self.stmts.expr.value} --> {self.stmts.stmts.value} [] !({self.stmts.expr.value}) --> skip fi ]|'

        result = par.parse(semIfStr, lexer=lex)
        # result.decorate()
        semIf = result.printPreApp(par, lex, esp)

        body2 = compose([body2, semIf])

        bodyForAll = binOpPreApp(OR, body1, body2)
        rangeForAll = binOpPreApp(AND, binOpPreApp(LEQ, ZERO, m), binOpPreApp(LEQ, m, i))
        forAll = forAllPreApp(m, rangeForAll, bodyForAll)

        # 4. C = D(i) ◦ (id{x∈Esp|abort∈D(i)({x})} ∪ {⟨abort, abort⟩})
        di = f'({CONCAT} ({D}) ({PAREN} {i}))'
        cdi = binOpPreApp(EQUAL, C, di)

        inRangeId = inRangePreApp(x, crossProduct(getListEsp(esp))) 
        bodyId = notInPreApp(ABORT, f'({CONCAT} ({di}) ({PAREN} ({SET2} {x})))')
        idFun = identityFun(setPreApp(inRangeId, bodyId))

        setAbort = setPreApp(None, tuplePreApp(ABORT, ABORT))

        unionCond = binOpPreApp(CUP, idFun, setAbort)
        cond = compose([cdi, unionCond])

        # 6. (∃D|D ∈ (Esp′^Esp' )[0..i] : bodyExist2)
        bodyExist2 = binOpPreApp(AND, forAll, cond)         # 4. AND 5.
        rangeArray = f'({RANGEARRAY} {i} {ZERO})'
        rangeExist2 = f'({SUPERSCRIPT} ({rangeArray}) ({SUPERSCRIPT} {espP} {espP}))'
        inRangeExist2 = inRangePreApp(D, rangeExist2) 
        exist2 = existPreApp(D, inRangeExist2, bodyExist2)

        # 7. (∃i|i ≥ 0 : exist2)
        rangeExist1 = binOpPreApp(GEQ, i, ZERO)
        exist1 = existPreApp(i, rangeExist1, exist2)

        # 8. U{C ∈ P(Esp′ × Esp′)| exist1}
        set2 = f'({BIGCUP} {setPreApp(inPesp, exist1)})'

        # 9. (∃y|y = set2 : z ∈ y ∪ (Dom(y)c × {abort}))
        rangeExist = binOpPreApp(EQUAL, y, set2)
        domY = f'({SUPERC} ({DOM} {y}))'
        crossDomAbort = crossProduct([domY, setPreApp(None, ABORT)])
        bodyExist = binOpPreApp(CUP, f'({IN} {y} {z})', crossDomAbort)
        exist = existPreApp(i, rangeExist, bodyExist)

        # 10. {z ∈ Esp′ × Esp′ | exist }
        setDo = setPreApp(inRange, exist)
        return setDo

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

    def printAST(self, level):
        return f'{"-" * level}For\n{self.range.printAST(level + 1)}\n{self.instr.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

class In(AST):
    def __init__(self, id, range, row, column) -> None:
        super().__init__(row, column)
        self.id = id
        self.range = range

    def decorate(self, symTabStack):
        symTabStack.insert(self.id.value, INT, self.range.expr1.value, self.row, self.column, True)
        self.id.decorate(symTabStack)
        self.range.decorate(symTabStack)

    def printAST(self, level):
        return f'{"-" * level}In\n{self.id.printAST(level + 1)}\n{self.range.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

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

    def printAST(self, level):
        return f'{"-" * level}To\n{self.expr1.printAST(level + 1)}\n{self.expr2.printAST(level + 1)}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

# ------------------ TYPES ------------------
class Type(AST):
    def __init__(self, name, row, column) -> None:
        super().__init__(row, column)
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def decorate(self, symTabStack):
        pass

    # def printAST(self, level):
    #     return f'{"-" * level}Type\n{self.type}'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

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

    # def printAST(self, level):
    #     print("-" * level + "ArrayType")
    #     self.start.printAST(level + 1)
    #     self.end.printAST(level + 1)

    def printPreApp(self, esp, typ=None):
        return f'to-do' 

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

    def printAST(self, level):
        return f'{"-" * level}Ident: {self.value} | type: {self.type}'

    def printPreApp(self, esp, typ=None):
        return esp[-1][self.value][1]

class Number(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = INT

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def printAST(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

    def printPreApp(self, esp, typ=None):
        return f'({convertNumberPreApp(self.value)})' 

class Boolean(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = BOOL

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def printAST(self, level):
        return f'{"-" * level}Literal: {self.value} | type: {self.type}'

    def printPreApp(self, esp, typ=None):
        return f'{convertBooleanPreApp(self.value)}'

class String(AST):
    def __init__(self, value, row, column) -> None:
        super().__init__(row, column)
        self.value = value
        self.type = STR

    def __str__(self):
        return f'{self.value}'

    def decorate(self, symTabStack):
        pass

    def printAST(self, level):
        return f'{"-" * level}String: "{self.value}"'

    def printPreApp(self, esp, typ=None):
        return f'to-do' 
