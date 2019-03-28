from tkinter import *
from math import *
import cv2
import uuid
import requests
import os
import json
from imgTools import imageTools
import tkinter as tk

ventana=Tk()
it = imageTools()
ventana.title("POC _ Reconocimiento Facial - IyNT")
ventana.geometry("750x250")
ventana.configure(background="darkorange1")
color_boton=("red2")
os.environ['no_proxy'] = '127.0.0.1,localhost'
#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
bLocal = False

if bLocal:
    url = "http://localhost:5000/"
    url2 = "http://localhost:5001/"
else:
    url = "http://10.1.6.31:5000/"
    url2 = "http://10.1.6.31:5001/"
NO_PROXY = {
    'no': 'pass',
}
s = requests.Session()
s.proxies = NO_PROXY


def btnClik(num):
    #global operador
    #operador=operador+str(num)
    #input_text.set(operador) #ESTA PARTE SIRVE PARA VISUALIZAR LA OPERACION EN LA PANTALLA
    if num == 0:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        del(cap)
        frame = cv2.flip(frame, 1) # Flip camera vertically        
        nombre_foto = "imagetmp.png" #str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite('upload/'+nombre_foto, frame)
        img = 'upload/'+nombre_foto
        fin = open(img, 'rb')
        files = {'file': fin}
        r = s.post(url, files=files, json=False)
        aData = r.text.split(',') 
        oData=[]       
        nn=0
        for x in range(len(aData)):
            sData = aData[x].replace("[","")
            sData = sData.replace("]","")
            sData = sData.replace("\"","")
            sData = sData.replace("\'","")
            oData.append(sData)
        indice=0
        indice_mayor=0
        for i in oData[1::2]:
            indice =+1
            print(i[0:4])
            if float(i[0:4]) > nn:
                nn=float(i[0:4])
                indice_mayor=indice
         
        sNombre = aData[indice-1]
        print(sNombre)
        input_text.set("Hola " + sNombre[2:] + ", en unos minutos el cajero lo va a atender. Gracias.")
        r.close()
        s.close()
    elif num == 3:
        it.testCamara()
    elif num == 4:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        frame = cv2.flip(frame, 1) # Flip camera vertically        
        nombre_foto = "imagetmp.png" #str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite('upload/'+nombre_foto, frame)
        img = 'upload/'+nombre_foto
        fin = open(img, 'rb')
        files = {'file': fin}
        r = s.post(url2, files=files, json=True)
        aData = r.text.split(',')
        sNombre = aData[0]
        print(sNombre)
        input_text.set("Hola " + sNombre[2:] + ", en unos minutos el cajero lo va a atender. Gracias.")
        r.close()
        s.close()

def clear():
    global operador
    operador=("")
    input_text.set("")

def operacion():
    global operador
    try:
        opera=str(eval(operador))#SIRVE PARA REALIZAR LA OPERACIÓN PREVIAMENTE VISUALIZADA EN PANTALLA
    except:
        clear()
        opera=("ERROR")
    input_text.set(opera)#MUESTRA EL RESULTADO

ancho_boton=15
alto_boton=2
input_text=StringVar()

operador=""
clear() #MUESTRA "0" AL INICIAR LA CALCULADORA

Boton0=Button(ventana,text="Modelo Arq.Empresarial",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(0)).place(x=150,y=160)
#Boton3=Button(ventana,text="Test Cámara",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(3)).place(x=280,y=160)
#Boton4=Button(ventana,text="Modelo SCI",bg=color_boton,width=ancho_boton,height=alto_boton,command=lambda:btnClik(4)).place(x=410,y=160)

Salida=Entry(ventana,font=('arial',12,'bold'),width=72,textvariable=input_text,bd=20,insertwidth=6,bg="powder blue",justify="left").place(x=30,y=60)

ventana.mainloop()