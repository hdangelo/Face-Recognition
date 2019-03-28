from PIL import Image
import cv2
import os
from classModel import clsModel

class recoFaceTools:
    """ Librería para el reconocimiento de imagens
        Métodos:
            equalizaImagen(self, frame)
            seekFace(self, frame)
            seekPersons(self,size,faces,gray,frame,model)
            loadModel(self, pathModel)
                Métodos:
                    @loadModel.setter
                    @loadModel.getter
            traiModel(self,pathFaces,pathModelOut)
    """    
    def __init__(self, size=4, width=112, height=112):    
        self.im_width = width
        self.im_height = height        
        self.size = size
        clsmodel=clsModel()
        clsmodel.loadModel("model/simplemodel.yml")                

    def equalizaImagen(self, frame):        
        #frame=cv2.flip(frame,1,0)
        #convertimos la imagen a blanco y negro    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #redimensionar la imagen
        mini = cv2.resize(gray, (int(gray.shape[1]), int(gray.shape[0])))
        return(mini, gray)

    def buscaCaras(self, frame):
        # Parte 2: Utilizar el modelo entrenado en funcionamiento con la camara
        face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml')        
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
        return(faces)

    def buscaPersonas(self,size,faces,gray,frame):
        ret=""
        for i in range(len(faces)):
            face_i = faces[i]
            (x, y, w, h) = [v * size for v in face_i]
            try:                            
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.im_width, self.im_height))
                # Intentado reconocer la cara
                model = clsmodel.get_Model()
                prediction = model.predict(face_resize)
                #Dibujamos un rectangulo en las coordenadas del rostro
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)            
                # Escribiendo el nombre de la cara reconocida
                # La variable cara tendra el nombre de la persona reconocida
                cara = '%s' % (self.names[prediction[0]])                            
                #Si la prediccion tiene una exactitud menor a 100 se toma como prediccion valida
                if prediction[1]<100 :
                    #En caso de que la cara sea de algun conocido se realizara determinadas acciones. Por Ejemplo, validar contra una lista, etc.            
                    #Ponemos el nombre de la persona que se reconoció
                    #cv2.putText(frame,'%s - %.0f' % (cara,prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 0))
                    #Si la prediccion es mayor a 100 no es un reconomiento con la exactitud suficiente
                    return(cara)
                elif prediction[1]>101 and prediction[1]<500:           
                    #Si la cara es desconocida, poner desconocido
                    cv2.putText(frame, 'Desconocido',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                    return("Desconocido")
            except :
                return(ret)

    def traiModel(self,pathFaces,pathModelOut):
        model = cv2.face.LBPHFaceRecognizer_create()
        (images, lables, names, id) = ([], [], {}, 0)
        for (subdirs, dirs, files) in os.walk(pathFaces):
            for subdir in dirs:
                names[id] = subdir
                subjectpath = os.path.join(pathFaces, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    lable = id
                    images.append(cv2.imread(path, 0))
                    lables.append(int(lable))
                id += 1
        model.train(images, lables)
        model.save(pathModelOut)
        return(model)
    
    def cargaNombres(self,nombres):
        names=nombres
        return()
