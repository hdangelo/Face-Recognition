import cv2

cams_test = 1
while True:
    #for i in range(0, 2):
    try:
        cap0 = cv2.VideoCapture(0)
        cap0.set(3,640) # set Width
        cap0.set(4,480) # set Height
        test0, frame0 = cap0.read()
        cv2.imshow('Camara 1',frame0)
        cap1 = cv2.VideoCapture(1)
        cap1.set(3,640) # set Width
        cap1.set(4,480) # set Height
        test1, frame1 = cap1.read()
        cv2.imshow('Camara 2',frame1)
    except:
        pass

    k = cv2.waitKey(1) & 0xff
    if k == 27: # press 'ESC' to quit
        break