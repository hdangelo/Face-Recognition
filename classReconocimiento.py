import cv2
import os
import numpy
from numpy import loadtxt
from PIL import Image
from imgTools import imageTools

class clsReconocimiento:
    def __init__(self, GrabaCaras=False):         
        self.bGrabaCaras = GrabaCaras

    def Reconocimiento(self, image):
        it=imageTools()
        #Tamaño para reducir a miniaturas las fotografias
        size = 2
        (im_width, im_height) = (112, 92)
        # Crear una lista de imagenes y una lista de nombres correspondientes
        # Carga los label del modelo entrenado
        model = cv2.face.LBPHFaceRecognizer_create()
        #model.setRadius(2)
        print('X:' + str(model.getGridX()))
        print('Y:' + str(model.getGridY()))
        print(model.getRadius())
        print(model.getNeighbors())
        print('Threshold:' + str(model.getThreshold()))
        model.read("model/arquitecturaempresarial.yml")        
        files = open("model/arquitecturaempresarial.txt", 'r')
        names = files.read().split(',')
        # Utilizar el modelo entrenado en funcionamiento con la camara
        face_cascade = cv2.CascadeClassifier( 'cascades/haarcascade_frontalface_default.xml')
        print('La imagen a abrir esta en ' + image)
        frame = it.load_image_file(image) 
        print('cargo la imagen')       
        #convertimos la imagen a blanco y negro            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
        print('convierte la imagen a gama de grises')    
        #redimensionar la imagen
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        print('redimensiona la imagen.....')
        #buscamos las coordenadas de los rostros (si los hay) y guardamos su posicion
        #cas_rejectLevel = 1.1
        #cas_levelWeight = 2
        faces = face_cascade.detectMultiScale(mini)
        faces = sorted(faces, key=lambda x: x[3], reverse=True)
        w_=0
        #caraPrimerPlano=0
        caras=[]
        for i in range(len(faces)):
            print('reconocio al menos 1 cara - ' + str(len(faces)))
            face_i = faces[i]
            (x, y, w, h) = [v * size for v in face_i]
            #if w > w_:
            #    caraPrimerPlano=i
            face = gray[y:y + h, x:x + w]
            #print("Cara " + str(i) + "W:" + str(w)+ " H:" + str(h))
            face_resize = cv2.resize(face, (im_width, im_height))
            # Intentado reconocer la cara
            prediction = model.predict(face_resize)
            #Dibujamos un rectangulo en las coordenadas del rostro
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 255, 0), 1)
            # Escribiendo el nombre de la cara reconocida
            # La variable cara tendra el nombre de la persona reconocida
            cara = '%s' % (names[prediction[0]])
            #print(cara)
            #print('% ' + str(prediction[0]))
            #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
            if prediction[1]<100:            
                if prediction[1] == 0:
                    nPrediction= 100
                else:
                    nPrediction = prediction[1]
                cara = cara + ',' + str(nPrediction)
                #print('Encontro')
                caras.append(cara)
            #    #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
            elif prediction[1]>101 and prediction[1]<500:           
                #Si la cara es desconocida, poner desconocido
                #cv2.putText(frame, 'Desconocido' ,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))  
                cara = 'Desconocido'
                nPrediction = prediction[1]
                cara = cara + ',0'
                caras.append(cara)
                #print('No encontro')
                #it.grabaImgNueva(face_resize)
            else:
                caras.append("Desconocido,0")
        #print('retorna el array con las caras.....')
        return(caras)