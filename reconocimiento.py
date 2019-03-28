#OpenCV module
import cv2
#Modulo para leer directorios y rutas de archivos
import os
#OpenCV trabaja con arreglos de numpy
import numpy
from numpy import loadtxt
import uuid
#Se importa la lista de personas con acceso al laboratorio
from PIL import Image, ImageFilter
from listaPermitidos import flabianos
from reconocimientoFacialTools import recoFaceTools
from imgTools import imageTools

it=imageTools()
sfTools=recoFaceTools()
flabs=flabianos()
bGrabaCaras = True
bVideo=True
bDetectaOjos=False
bIdentifica=False
sNombre='Sebastian Carvallo'

# Parte 1: Creando el entrenamiento del modelo
print('Formando...')

#Directorio donde se encuentran las carpetas con las caras de entrenamiento
dir_faces = 'att_faces/orl_faces'
#Tamaño para reducir a miniaturas las fotografias
size = 2
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
face_cascade = cv2.CascadeClassifier( 'cascades/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
if bVideo:
    cap = cv2.VideoCapture(0)
#cap = Image.open("C:/Desarrollo/Ejemplos/Python ejemplos/201903/FaceRecognition2-master/FaceRecognition2-master/att_faces/para entrenar/1.png")
else:
    frame = it.load_image_file("J:/Sistemas/CC1253/I+NT/ReconocimientoFacial/Mas imagenes/WyJQ9Mq2_400x400.jpg")
    frame = it.mejoraImagen(frame)

while True:
    #leemos un frame y lo guardamos
    if bVideo:
        nKey = 3
        rval, frame = cap.read()
        cap.set(3, 800)
        cap.set(4, 600)

        #mini, gray = sfTools.equalizaImagen(frame)  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #redimensionar la imagen
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))  
        frame=cv2.flip(frame,1,0)
    else:
        nKey=0
    #convertimos la imagen a blanco y negro          
    #frame = it.mejoraImagen(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #redimensionar la imagen
    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
    
    #buscamos las coordenadas de los rostros (si los hay) y
    #guardamos su posicion
    cas_rejectLevel = 1.1 #1.1
    cas_levelWeight = 2   #2
    """
    faces = face_cascade.detectMultiScale(
        mini,
        scaleFactor=1.4,
        minNeighbors=1,
        minSize=(10,10),
        flags = cv2.CASCADE_SCALE_IMAGE
        )
    """
# 1 cara    2 caras     3 caras     >3 <8 caras    +8 caras
# 1.4       1.4         1.5          1.6            1.5
# 1         1           2            2              1
#(30,30)   (10,10)     (30,30)      (20,20)        (1,1)

    faces = face_cascade.detectMultiScale(mini)

    #faces = face_cascade.detectMultiScale(mini,cas_rejectLevel,cas_levelWeight)
    #print(len(faces))
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

        if bIdentifica:
        # Intentado reconocer la cara
            prediction = model.predict(face_resize)
        
            #Dibujamos un rectangulo en las coordenadas del rostro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 100, 100), 2)
# Marco ojos        
        if bDetectaOjos:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(40,55,200),2)
            #cv2.imshow('img',frame)
#        
        #
        #Graba la cara seleccionada
        if bGrabaCaras:
            rutaDestino = "J:/Sistemas/CC1253/I+NT/ReconocimientoFacial/Imagenes Recortadas2"  # '/' + sNombre
            if not os.path.isdir(rutaDestino):
                os.mkdir(rutaDestino)
            try:
                pin=sorted([int(n[:n.find('.')]) for n in os.listdir(rutaDestino)
                       if n[0]!='.' ]+[0])[-1] + 1
            except:
                pin=str(uuid.uuid4()) + ".png"
                pass
            #Metemos la foto en el directorio
            cv2.imwrite('%s/%s.png' % (rutaDestino, pin), face_resize)
        
        # Escribiendo el nombre de la cara reconocida
        # La variable cara tendra el nombre de la persona reconocida
        if bIdentifica:
            cara = '%s' % (names[prediction[0]])
            nPrediction=0
            #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
            if prediction[1]<100 :
                #Ponemos el nombre de la persona que se reconoció
                cv2.putText(frame,'%s - %.0f' % (cara,prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(72,118,255))
                #En caso de que la cara sea de algun conocido se realizara determinadas accione          
                #Busca si los nombres de las personas reconocidas estan dentro de los que tienen acceso          
                #flabs.TuSiTuNo(cara)
            #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
            elif prediction[1]>101 and prediction[1]<500:           
                #Si la cara es desconocida, poner desconocido
                cv2.putText(frame, 'Desconocido' ,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255,0,0)) 
        #Mostramos la imagen
        
    #Si se presiona la tecla ESC se cierra el programa
    #print("la cara mas cerca es la " + str(cara))
    cv2.imshow('OpenCV Reconocimiento facial', frame)
    key = cv2.waitKey(nKey)
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
    