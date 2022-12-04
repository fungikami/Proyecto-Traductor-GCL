"""
    Implementación de la tabla de símbolos para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 05/12/2022
"""

class SymbolTable:
    """ Clase que implementa la tabla de símbolos del intérprete de GCL. """
    def __init__(self):
        self.level = -1
        self.table = {}

    def insert(self, name, type: str, value):
        """ 
            Inserta una variable en la tabla de símbolos, 
            dado su nombre, tipo y valor.
        """
        if name not in self.table:
            self.table[name] = {}

        if self.level in self.table[name]:
            raise Exception(f'Error: Variable "{name}" already declared')

        self.table[name][self.level] = [type, value]

    def update(self, name, value):
        """ Actualiza el valor de una variable en la tabla de símbolos. """
        var = self.lookup(name)
        var[1] = value
        # self.table[name][1] = value

    def lookup(self, name):
        """ Busca una variable en la tabla de símbolos. """
        lvl = self.level
        while lvl >= 0:
            if name in self.table and lvl in self.table[name]:
                return self.table[name][lvl]
            lvl -= 1

        raise Exception(f'Error: Variable "{name}" not declared')

    def get_type(self, name):
        """ Obtiene el tipo de una variable en la tabla de símbolos. """
        return self.lookup(name)[0]

    def get_value(self, name):
        """ Obtiene el valor de una variable en la tabla de símbolos. """
        return self.lookup(name)[1]

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

