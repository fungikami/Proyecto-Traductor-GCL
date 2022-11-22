import subprocess as sp
import os

if __name__ == '__main__':
    print("Testing the function")
    for fileName in os.listdir("CasosDePrueba Etapa 2/Tests"):
        print("Testing the file: " + fileName)
        sp.call(
            f'python3 gcl.py CasosDePrueba\ Etapa\ 2/Tests/{fileName} > CasosDePrueba\ Etapa\ 2/Out2/{fileName}.txt', shell=True)
        print("Done\n")
