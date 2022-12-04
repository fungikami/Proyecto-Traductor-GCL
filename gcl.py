"""
    Programa principal que lee un archivo y muestra el AST.

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 18/11/2022
"""

from ply import lex, yacc
from sys import argv, path
path.append('src')
from grammar import *
from lexer import *

if __name__ == '__main__':
    lexer = lex()
    parser = yacc.yacc()

    # Leer el archivo de entrada
    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        print("Usage: python gcl.py <input_file>")
        exit(1)

    if not argv[1].endswith(".gcl"):
        print("Error: Invalid file extension (must be .gcl)")
        print("Usage: python lexer.py <input_file>")
        exit(1)

    f = open(argv[1], 'r')
    data = f.read()
    f.close()

    result = parser.parse(data, lexer=lexer)

    if result:
        print(result.imprimir(0))
        try:
            result.decorate()
        except Exception as e:
            print(e)
            exit(1)