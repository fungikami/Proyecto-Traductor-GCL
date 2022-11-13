import ply.yacc as yacc
from grammar import *
from lexer import *
from sys import argv

if __name__ == '__main__':
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

    while True:
        try:
            s = data
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
