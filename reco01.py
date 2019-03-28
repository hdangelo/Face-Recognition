#OpenCV module
import cv2
#Modulo para leer directorios y rutas de archivos
import os
#OpenCV trabaja con arreglos de numpy
import numpy
#Se importa la lista de personas con acceso al laboratorio
from listaPermitidos import flabianos
from reconocimientoFacialTools import recoFaceTools
from classModel import clsModel
model=clsModel()
flabs=flabianos()

print('Formando...')

#Directorio donde se encuentran las carpetas con las caras de entrenamiento
dir_faces = 'att_faces/orl_faces'

# Parte 2: Utilizar el modelo entrenado en funcionamiento con la camara
sfTools=recoFaceTools()
print("Cargando Modelo")
model.loadModel("model/simplemodel.yml")
files = open("model/simplemodel.txt", 'r')
names = files.read().split(',')
sfTools.cargaNombres(names)
print("Modelo cargado....")
cap = cv2.VideoCapture(0)

while True:
    #leemos un frame y lo guardamos
    print("Lee 1 frame")
    cv2.waitKey(3000)
    rval, frame = cap.read(0)
    mini, gray = sfTools.equalizaImagen(frame)    
    """buscamos las coordenadas de los rostros (si los hay) y
   guardamos su posicion"""
    faces = sfTools.buscaCaras(frame)
    print("Busca Caras")
    cara = sfTools.buscaPersonas(4,faces,gray,frame)    
    
    cv2.imshow('OpenCV Reconocimiento facial', frame)

    #Si se presiona la tecla ESC se cierra el programa
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break
