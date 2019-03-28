import numpy as np
import cv2
import uuid
import requests
import os
from tkinter import Tk
from tkinter import messagebox
from tkinter import Menu

bLocal = False
os.environ['no_proxy'] = '127.0.0.1,localhost'
#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

if bLocal:
    url = "http://localhost:5000/"
else:
    url = "http://10.1.6.31:5000/"
NO_PROXY = {
    'no': 'pass',
}
s = requests.Session()
s.proxies = NO_PROXY

def llamaAPI(img):
    try:
        fin = open(img, 'rb')
        files = {'file': fin}

        r = s.post(url, files=files, json=True)
        print(r.text)    
    finally:
	    fin.close()

root = Tk()
root.title("Bienvenidos a la Poc de reconocimiento facial")
root.geometry('350x200')
Frame = Tk.frame(root)


Button(Frame, text="QUIT", fg="red", command=quit).pack(side=Tk.LEFT)
#button.pack(side=Tk.LEFT)
Button(Frame,
                   text="Hello",
                   command=llamaAPI).pack(side=Tk.LEFT)
#slogan.pack(side=Tk.LEFT)

root.mainloop()

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    elif k == 13:        
        nombre_foto = str(uuid.uuid4()) + ".png" # uuid4 regresa un objeto, no una cadena. Por eso lo convertimos
        cv2.imwrite('upload/'+nombre_foto, frame)
        llamaAPI('upload/'+nombre_foto)
cap.release()
cv2.destroyAllWindows()