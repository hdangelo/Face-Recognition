#OpenCV module
import cv2
#Modulo para leer directorios y rutas de archivos
import os
#OpenCV trabaja con arreglos de numpy
import numpy
from numpy import loadtxt
#Se importa la lista de personas con acceso al laboratorio
from PIL import Image, ImageFilter
from listaPermitidos import flabianos
from reconocimientoFacialTools import recoFaceTools
from imgTools import imageTools

it=imageTools()
sfTools=recoFaceTools()
flabs=flabianos()
bGrabaCaras = False
bVideo=True
bIdentifica=True
# Parte 1: Creando el entrenamiento del modelo
print('Formando...')

#Directorio donde se encuentran las carpetas con las caras de entrenamiento
dir_faces = 'att_faces/orl_faces'
#Tamaño para reducir a miniaturas las fotografias
size = 5    # 4 = distancia a la camara +- 50cm
(im_width, im_height) = (112, 112)
# Crear una lista de imagenes y una lista de nombres correspondientes
model = cv2.face.LBPHFaceRecognizer_create()
model.read("model/arquitecturaempresarial20190326.yml")
# Carga los label del modelo entrenado
names = []
files = open("model/arquitecturaempresarial20190326.txt", 'r')
names = files.read().split(',')
#model.train(images, lables)

# Parte 2: Utilizar el modelo entrenado en funcionamiento con la camara
face_cascade = cv2.CascadeClassifier( 'cascades/haarcascade_frontalface_default.xml')
if bVideo:
    cap = cv2.VideoCapture(0)
#cap = Image.open("C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/att_faces/para entrenar/1.png")
else:
    frame = it.load_image_file("upload/IMG_20170417_135623784_BURST000_COVER_TOP.jpg")

while True:
    #leemos un frame y lo guardamos
    if bVideo:
        rval, frame = cap.read()
        mini, gray = sfTools.equalizaImagen(frame)    
        frame=cv2.flip(frame,1,0)
    #convertimos la imagen a blanco y negro          
    frame_new = it.mejoraImagen(frame)
    
    gray = cv2.cvtColor(frame_new, cv2.COLOR_BGR2GRAY)
    
    #redimensionar la imagen
    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
    
    #buscamos las coordenadas de los rostros (si los hay) y
    #guardamos su posicion
    cas_rejectLevel = 1.1 #1.1
    cas_levelWeight = 2   #2
    faces = face_cascade.detectMultiScale(mini)
    #faces = face_cascade.detectMultiScale(mini,cas_rejectLevel,cas_levelWeight)
    faces = sorted(faces, key=lambda x: x[3])
    w_=0
    cara=0
    for i in range(len(faces)):
        face_i = faces[i]
        (x, y, w, h) = [v * size for v in face_i]
        if w > w_:
            cara=i
        face = gray[y:y + h, x:x + w]
        #print("Cara " + str(i) + "W:" + str(w)+ " H:" + str(h))
        face_resize = cv2.resize(face, (im_width, im_height))
        if bIdentifica and len(faces)==1:
            # Intentado reconocer la cara
            prediction = model.predict(face_resize)
            # Dibujamos un rectangulo en las coordenadas del rostro
            cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 255, 0), 1)
            cara = '%s' % (names[prediction[0]])
            print(cara + str(prediction[1]))
            nPrediction=0
            #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
            if prediction[1]>=80 and prediction[1]<=102 :              
                cv2.putText(frame,'%s - %.0f' % (cara,prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(250,255,0))
                #En caso de que la cara sea de algun conocido se realizara determinadas accione          
                #Busca si los nombres de las personas reconocidas estan dentro de los que tienen acceso          
                #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
            """
            elif prediction[1]>100 and prediction[1]<500:           
                #Si la cara es desconocida, poner desconocido
                cv2.putText(frame, 'Desconocido' ,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 0, 0))  
            """
    #Mostramos la imagen
    #Graba la cara seleccionada
        if bGrabaCaras:
            rutaDestino = "tmp"
            pin=sorted([int(n[:n.find('.')]) for n in os.listdir(rutaDestino)
                   if n[0]!='.' ]+[0])[-1] + 1

            #Metemos la foto en el directorio
            cv2.imwrite('%s/%s.png' % (rutaDestino, pin), face_resize)
        
    # Escribiendo el nombre de la cara reconocida
    # La variable cara tendra el nombre de la persona reconocida

    #Si se presiona la tecla ESC se cierra el programa
    #print("la cara mas cerca es la " + str(cara))
    cv2.imshow('OpenCV Reconocimiento facial', frame)
    #cv2.imshow('Mejorada', frame_new)
    key = cv2.waitKey(2000)
    if key == 27:
        cv2.destroyAllWindows()
        break
    elif key == 13:
        rutaDestino = "tmp"
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(rutaDestino)
                if n[0]!='.' ]+[0])[-1] + 1

            #Metemos la foto en el directorio
        cv2.imwrite('%s/%s.png' % (rutaDestino, pin), face_resize)
        t1 = rutaDestino + '/' + str(pin) + '.png'
        img = cv2.imread('%s/%s.png' % (rutaDestino, pin))
        img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
        img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)

        cv2.imwrite('%s/%s.png' % (rutaDestino, pin), hist_equalization_result)
    