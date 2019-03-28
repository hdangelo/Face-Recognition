from tkinter import *
import tkinter as tk
import cv2
import uuid
import requests
import os
import json

os.environ['no_proxy'] = '127.0.0.1,localhost'
#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
bLocal = True
if bLocal:
    url = "http://localhost:5000/"
else:
    url = "http://10.1.6.31:5000/"
NO_PROXY = {
    'no': 'pass',
}
s = requests.Session()
s.proxies = NO_PROXY


def llamaAPI(text):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1) # Flip camera vertically
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #cv2.imshow('frame', frame)
        nombre_foto = str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite('upload/'+nombre_foto, frame)
        img = 'upload/'+nombre_foto
        cap.release()
        fin = open(img, 'rb')
        files = {'file': fin}

        r = s.post(url, files=files, json=True)
        print('Hola ' + json.dumps(r.text))
        aData = r.text.split(',')
        print("Hola " + aData[0])
        text.insert(END, "Hola " + aData[0])
    finally:
	    fin.close()

root = Tk()
root.title('Text')
text = Text(root, height=26, width=50)
scroll = Scrollbar(root, command=text.yview)
text.configure(yscrollcommand=scroll.set)
text.tag_configure('bold_italics', font=('Verdana', 12, 'bold', 'italic'))
text.tag_configure('big', font=('Verdana', 24, 'bold'))
text.tag_configure('color', foreground='blue', font=('Tempus Sans ITC', 14))
text.tag_configure('groove', relief=GROOVE, borderwidth=5)
text.tag_bind('bite', '<1>',
              lambda e, t=text: t.insert(END, "I'll bite your legs off!"))
bdw=0
Label(bdw, text='POC de Reconocimiento FACIAL').pack(side=TOP)
button = Button(text, text='Pulse acá', width=25, relief='groove', borderwidth=5 ,command=llamaAPI(text))
text.window_create(END, window=button)
text.insert(END, 'I dare you to click on this\n', 'bite')
text.pack(side=LEFT)
scroll.pack(side=RIGHT, fill=Y)

root.mainloop()