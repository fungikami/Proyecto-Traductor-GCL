"""
    Implementación de la tabla de símbolos para el lenguaje GCL.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

class SymbolTable:
    """ Clase que implementa la tabla de símbolos del intérprete de GCL.
    """

    def __init__(self):
        self.table = {}

    def insert(self, name, type, value):
        """ 
            Inserta una variable en la tabla de símbolos, 
            dado su nombre, tipo y valor.
        """
        if name in self.table:
            raise Exception("Variable ya declarada")

        self.table[name] = [type, value]

    def update(self, name, value):
        """ Actualiza el valor de una variable en la tabla de símbolos. """
        if name not in self.table:
            raise Exception("Variable no declarada")

        self.table[name][1] = value

    def lookup(self, name):
        """ Busca una variable en la tabla de símbolos. """
        if name not in self.table:
            raise Exception("Variable no declarada")

        return self.table[name]

    def get_type(self, name):
        """ Obtiene el tipo de una variable en la tabla de símbolos. """
        return self.lookup(name)[0]

    def get_value(self, name):
        """ Obtiene el valor de una variable en la tabla de símbolos. """
        return self.lookup(name)[1]

    def __str__(self):
        """ Representación de la tabla de símbolos. """
        return str(self.table)

