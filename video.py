import numpy as np
import cv2 as cv
import imutils

cap = cv.VideoCapture(-1)

template = cv.imread('level_2.png',0)
w, h = template.shape[::-1]


def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x, y)



while True:
    ret, frame = cap.read()
    if not ret:
        print("no frame")

    
    crop_x, crop_y, crop_w, crop_h = 225, 328, 30,29
    #crop_x, crop_y, crop_w, crop_h = 274, 280, 85, 28
    #crop_x, crop_y, crop_w, crop_h = 268, 280, 60, 25
    frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #gray = cv.bilateralFilter(gray,7,75,75)
    #gray = cv.GaussianBlur(gray,(5,5),0)
       
    #gray = cv.bitwise_not(gray)

    #threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    #cv.imwrite("level_3.png", gray)
    
    #ret,threshed = cv.threshold(gray,230,255,cv.THRESH_BINARY)

    cv.imwrite("no_threes.png", gray)

    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)

    '''
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)


    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv.rectangle(gray,top_left, bottom_right, 255, 2)
    '''

    cv.imshow('image', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()