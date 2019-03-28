import cv2
import numpy
import os

# Parte 1: Creando el entrenamiento del modelo
print('Formando...')

#Directorio donde se encuentran las carpetas con las caras de entrenamiento
dir_faces = 'C:/Desarrollo/Ejemplos/Python ejemplos/201903/dbpersonas'

#Tamaño para reducir a miniaturas las fotografias
size = 4

# Crear una lista de imagenes y una lista de nombres correspondientes
file = open("model/arquitecturaempresarial20190326.txt","w")
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(dir_faces):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(dir_faces, subdir)
        file.write(subdir +",")
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
file.close
(im_width, im_height) = (112, 112)

# Crear una matriz Numpy de las dos listas anteriores
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV entrena un modelo a partir de las imagenes
model = cv2.face.LBPHFaceRecognizer_create()
"""
nGridX = model.getGridX()
nGridY = model.getGridY()
nRadius = model.getRadius()
dThreshold = model.getThreshold()
#model.setRadius(2)
print('X:' + str(model.getGridX()))
print('Y:' + str(model.getGridY()))
print('Radius:' + str(model.getRadius()))
print('Neighbors:'+ str(model.getNeighbors()))
print('Threshold:' + str(model.getThreshold()))
"""
model.train(images,lables)
model.save("model/arquitecturaempresarial20190326.yml")