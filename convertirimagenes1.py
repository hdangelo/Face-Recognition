#!/usr/bin/env python
from PIL import Image
import sys
import os.path

# This is a tiny script to help you creating a CSV file from a face
# database with a similar hierarchie:
#
#  philipp@mango:~/facerec/data/at$ tree
#  .
#  |-- README
#  |-- s1
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  |-- s2
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  ...
#  |-- s40
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#

pathOut = "C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/att_faces/Para entrenar/A1"
BASE_PATH="C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/att_faces/Para entrenar/BGBA"
SEPARATOR=";"

label = 0
for dirname, dirnames, filenames in os.walk(BASE_PATH):
    for subdirname in dirnames:
        subject_path = os.path.join(dirname, subdirname)
        nImage=1
        for filename in os.listdir(subject_path):
            abs_path = "%s/%s" % (subject_path, filename)
            #
            folders = subject_path.split(os.sep)            
            #
        
            print ("%s%s%d" % (abs_path, SEPARATOR, label))
            if not os.path.isdir(pathOut+"/"+folders[1]):
                os.mkdir(pathOut+"/"+folders[1])
            size = 4
            foto = Image.open(abs_path) 
            datos = foto.getdata() 
            #para el calculo del promedio se utilizara la division entera con el operador de division doble "//" para evitar decimales
            
            promedio = [(datos[x][0] + datos[x][1] + datos[x][2]) // 3 for x in range(len(datos))]
            imagen_gris = Image.new('L', foto.size) 
            imagen_gris.putdata(promedio) 
            imagen_gris.save(pathOut+"/"+folders[1]+"/"+str(nImage)+".jpg")
            foto.close()
            imagen_gris.close()
            nImage +=1
        label = label + 1