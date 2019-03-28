import tkinter as tk
import cv2
import uuid
import requests
import os
import json
from tkinter import *
from tkinter import messagebox
from tkinter import font

os.environ['no_proxy'] = '127.0.0.1,localhost'
#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
bLocal = False
if bLocal:
    url = "http://localhost:5000/"
else:
    url = "http://10.1.6.31:5000/"
NO_PROXY = {
    'no': 'pass',
}
s = requests.Session()
s.proxies = NO_PROXY


def llamaAPI():
    text = Text()
    try:
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1) # Flip camera vertically        
        nombre_foto = "imagetmp.png" #str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite('upload/'+nombre_foto, frame)
        img = 'upload/'+nombre_foto
        cap.release()
        fin = open(img, 'rb')
        files = {'file': fin}

        r = s.post(url, files=files, json=True)
        print('Hola ' + json.dumps(r.text))
        aData = r.text.split(',')
        """
        text.config(font=('courier', 15, 'bold'))            
        text.config(width=5, height=5)
        text.pack(expand=YES, fill=BOTH)
        """
        sNombre = aData[0]
        
        messagebox.showinfo('POC - Reconocimiento de personas', "Hola " + sNombre[2:] + "\n En unos minutos el cajero lo va a atender.\n Gracias.")
        r.close()
        s.close()
        #msg = tk.Message(root, text = "Hola " + sNombre[2:] + "\n En unos minutos el cajero lo va a atender.\n Gracias.")
        #msg.config(bg='lightgreen', font=('times', 24, 'italic'))
        #msg.pack()
        

    finally:
	    fin.close()    

class Ayuda_Dialog:
    def __init__(self, parent):
        text = ("Paso1: De click en el botón de menú, posteriormente diríjase a...\n" 
                "Paso2: ...\n"
                "Paso3: ...")
        cap = cv2.VideoCapture(0)

        while True:
            leido, frame = cap.read()
            cv2.imshow('POC - Reconocimiento de personas', frame)
            cv2.waitKey(5)
        self.top = tk.Toplevel(parent)
        self.top.title("Ayuda")
        display = tk.Text(self.top)
        display.pack()
        display.insert(tk.INSERT, text)
        display.config(state=tk.DISABLED)
        b = tk.Button(self.top, text="Cerrar", command=self.cerrar)
        b.pack(pady=5)

    def cerrar(self):
        self.top.destroy()


class Main_Window:
    def __init__(self,  root):
        root.geometry("600x300")
        mnuAyuda = tk.Menu(root)
        mnuAyuda.add_command(label="PULSE AQUÍ", command=llamaAPI)
        root.config(menu=mnuAyuda)

    def ayuda(self):
        Ayuda_Dialog(root)


if __name__ == "__main__":   
    n1=0         
    root = tk.Tk()
    Main_Window(root)
    root.mainloop()