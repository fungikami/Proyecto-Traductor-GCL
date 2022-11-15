from ply import lex, yacc
from grammar import *
from lexer import *
from sys import argv

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
    print(result.imprimir(1))
