import numpy as np
import cv2 as cv
import sys

cap = cv.VideoCapture(-1)

letters = sys.argv[1]
for i in range(30):
    ret, frame = cap.read()
    
for i in range(5):
    ret, frame = cap.read()
    if not ret:
        print("no frame")

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imwrite("test_images/"+letters+"_"+str(i)+".png", gray)

cap.release()
cv.destroyAllWindows()
