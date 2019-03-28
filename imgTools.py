import PIL 
import numpy as np
import cv2
import os
import uuid
#from tkinter import*
class imageTools:
    def load_image_file(self,file, mode='RGB'):
        im = PIL.Image.open(file,'r')
        if mode:
            im = im.convert(mode)
        return np.array(im)
#
    def grabaImgNueva(self, imagen):
        rutaDestino = "C:/Desarrollo/Ejemplos/Python ejemplos/201903/tmp"
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(rutaDestino)
                if n[0]!='.' ]+[0])[-1] + 1

            #Metemos la foto en el directorio
        cv2.imwrite('%s/%s.png' % (rutaDestino, pin), imagen)
        # Escribiendo el nombre de la cara reconocida
        return
#
    def actualizoModelo(self, rutaImagen):

        return
#
    def testCamara(self):
        cap = cv2.VideoCapture(0)
        cap.set(3,640) # set Width
        cap.set(4,480) # set Height
        cap.release()
        while(True):
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1) # Flip camera vertically
#            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow('Test Camara - Pulse ESC para salir o ENTER para tomar Fotgrafia', frame)
            
            k = cv2.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                break
            elif k == 13:        
                nombre_foto = str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
                cv2.imwrite(nombre_foto, frame)
        cv2.destroyAllWindows()
#
    def mejoraImagen(self, img):
        img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
        img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
        hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)        
        return hist_equalization_result
#
    
    """
    def elijoModelo(self, marco):  
        master = Tk()
        var = IntVar()
        Label(marco, text = "Seleccione el MODELO a usar").grid(row=0, sticky=W)
        Radiobutton(marco, text = "Modelo Arq.Empr", variable = var, value = 1).grid(row=1, sticky=W)
        Radiobutton(marco, text = "Modelo Variado", variable = var, value = 2).grid(row=2, sticky=W)
        Radiobutton(marco, text = "Modelo Gcia. SCI", variable = var, value = 2).grid(row=3, sticky=W)
        Button(marco, text = "OK", command = master.quit).grid(row=4, sticky=W)
        selection = var.get()
        print ("Selection:", selection)
        return(selection)
        mainloop()
    """