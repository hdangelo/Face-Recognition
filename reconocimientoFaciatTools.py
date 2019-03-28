from PIL import Image
import cv2

class recoFaceTools:
    """ Librería para el reconocimiento de imagens"""

    #def __init__(self):        

    def equalizaImagen(self,frame):   
        size = 4
        frame=cv2.flip(frame,1,0)
        #convertimos la imagen a blanco y negro    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #redimensionar la imagen
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        return(mini)