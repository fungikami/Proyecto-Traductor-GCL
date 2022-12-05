import os
import subprocess as sp

if __name__ == '__main__':
    for fileName in os.listdir("CasosDePrueba Etapa 2/Out2"):
        print("Testing the file: " + fileName)
        f = fileName.split(".")[0]
        r = sp.run(
            f'cat CasosDePrueba\ Etapa\ 2/Out/{fileName}', shell=True)
        print(r)
        print("Done\n")
