import os
import subprocess as sp

if __name__ == '__main__':
    for fileName in os.listdir("CasosDePrueba Etapa 2/Out"):
        print("Testing the file: " + fileName)
        f = fileName.split(".")[0]
        r = sp.run(
            f'diff CasosDePrueba\ Etapa\ 2/Out/{fileName} CasosDePrueba\ Etapa\ 2/Out2/{f}.gcl.txt', shell=True)
        print(r)
        print("Done\n")
