import cv2
import json

scaleFactor = 1
cap = cv2. .VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(1920*scaleFactor))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(1080*scaleFactor))

print (cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print (cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        continue

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()