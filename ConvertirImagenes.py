from PIL import Image
import os

from pathlib import Path
from os import listdir

def ls(ruta = '.'):
    return listdir(ruta)

#def ls(ruta = Path.cwd()):
#    return [arch.name for arch in Path(ruta).iterdir() if arch.is_file()]

pathIn = "upload"
pathOut = "C:/Desarrollo/Ejemplos/Python ejemplos/201903/tmp"
#dir_faces = 'att_faces/orl_faces'
path = os.path.join(pathIn)

#Tamaño para reducir a miniaturas las fotografias
size = 4

#Si no hay una carpeta con el nombre ingresado entonces se crea
if not os.path.isdir(path):
    os.mkdir(pathOut)

      
for filename in os.listdir(pathIn):
    path = pathIn + '/' + filename           
    foto = Image.open(path) 
    datos = foto.getdata() 
    #para el calculo del promedio se utilizara la division entera con el operador de division doble "//" para evitar decimales
    
    promedio = [(datos[x][0] + datos[x][1] + datos[x][2]) // 3 for x in range(len(datos))]
    imagen_gris = Image.new('L', foto.size) 
    imagen_gris.putdata(promedio) 
    imagen_gris.save(pathOut + "/" + filename)
foto.close()
imagen_gris.close()