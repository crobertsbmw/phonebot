import numpy as np
import cv2 as cv
import imutils

cap = cv.VideoCapture(-1)

template = cv.imread('level.png',0)
w, h = template.shape[::-1]


def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x, y)



while True:
    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray = cv.bilateralFilter(gray,7,75,75)
    # gray = cv.GaussianBlur(gray,(5,5),0)
    
    #crop_x, crop_y, crop_w, crop_h = 270, 205, 60, 25
    #gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    

    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)



    #cv.imwrite("level.png", gray)

    cv.imshow('image', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()