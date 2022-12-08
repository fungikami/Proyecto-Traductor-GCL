"""
    Implementación de la tabla de símbolos para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 05/12/2022
"""

class SymbolVar:
    """ Clase que implementa una variable en la tabla de símbolos. """
    def __init__(self, name, type: str, value, readonly=False):
        self.name = name
        self.type = type
        self.value = value
        self.readonly = readonly

    def __str__(self):
        """ Representación de una variable. """
        return f'variable: {self.name} | type: {self.type}'

class SymbolTable:
    """ Clase que implementa la tabla de símbolos del intérprete de GCL. """
    def __init__(self):
        self.level = -1
        self.table = {}

    def insert(self, name, type: str, value, row, col, readonly=False):
        """ 
            Inserta una variable en la tabla de símbolos, 
            dado su nombre, tipo y valor.
        """
        if name not in self.table:
            self.table[name] = {}

        if self.level in self.table[name]:
            raise Exception(f'Error in row {row}, column {col}: Variable "{name}" already declared')

        self.table[name][self.level] = SymbolVar(name, type, value, readonly)

    def update(self, name, value, row, col):
        """ Actualiza el valor de una variable en la tabla de símbolos. """
        var = self.lookup(name, row, col)
        if var.readonly:
            raise Exception(f'Error in row {row}, column {col}: Variable "{name}" is readonly')

        var.value = value

    def lookup(self, name, row, col):
        """ Busca una variable en la tabla de símbolos. """
        lvl = self.level
        while lvl >= 0:
            if name in self.table and lvl in self.table[name]:
                return self.table[name][lvl]
            lvl -= 1

        raise Exception(f'Error in row {row}, column {col}: Variable "{name}" not declared')

    def get_type(self, name, row, col):
        """ Obtiene el tipo de una variable en la tabla de símbolos. """
        return self.lookup(name, row, col).type

    def get_value(self, name, row, col):
        """ Obtiene el valor de una variable en la tabla de símbolos. """
        return self.lookup(name, row, col).value

    def is_readonly(self, name, row, col):
        """ Verifica si una variable es de solo lectura. """
        return self.lookup(name, row, col).readonly

    def exist_name(self, name):
        """ Verifica si una variable existe en la tabla de símbolos. """
        return name in self.table

    def open_scope(self):
        """ Abre un nuevo nivel de ámbito. """
        self.level += 1

    def close_scope(self):
        """ Cierra el nivel de ámbito actual. """
        for key in self.table:
            if self.level in self.table[key]:
                del self.table[key][self.level]
        self.level -= 1

    def __str__(self):
        """ Representación de la tabla de símbolos. """
        return str(self.table)
