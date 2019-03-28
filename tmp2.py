import cv2
import sys
import os
import time
camera_index = 0 
capture = cv2.VideoCapture(0)
count = 0
def repeat():
    global capture
    global camera_index
    global count
    frame = cv2.GetMat(cv2.QueryFrame(capture))
    framegray = cv2.CreateMat(480, 640, cv2.CV_8UC1)
    cv2.CvtColor(frame, framegray, cv2.CV_BGR2GRAY)
    sys.stdout.write(framegray.tostring())
    c = cv2.WaitKey(1)
    if c == 27:
        print (count)
        sys.exit()

while True:
    repeat()