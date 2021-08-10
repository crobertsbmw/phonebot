import numpy as np
import cv2 as cv
import imutils

cap = cv.VideoCapture(-1)


def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        print(x, y)



while True:
    ret, frame = cap.read()
    if not ret:
        print("no frame")

    
    #crop_x, crop_y, crop_w, crop_h = 195, 0, 250,390
    #crop_x, crop_y, crop_w, crop_h = 274, 280, 85, 28
    #crop_x, crop_y, crop_w, crop_h = 263, 271, 60, 25
    
    #frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #gray = cv.bilateralFilter(gray,7,75,75)
    gray = cv.bitwise_not(gray)
    
    
    ret,threshed = cv.threshold(gray,70,255,cv.THRESH_BINARY)
    crop_x, crop_y, crop_w, crop_h = 255, 235, 150, 160
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    
    contours, hierarchy = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    colored = cv.cvtColor(gray,cv.COLOR_GRAY2RGB) 
    cv.drawContours(colored, contours, -1, (0,255,0), 3)
    print("*****")
    points = []
    for contour in contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        if bh > 200:
            screen_x = bx
            screen_y = by
            screen_w = bw
            screen_h = bh
        else:
            points.append((bw/2+bx, bh/2+by))
    
    
    '''
    m = cv.mean(threshed)[0]
    #print(m)
    #ret,threshed = cv.threshold(gray, 200,255,cv.THRESH_TRUNC)
    #threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    
    
    #cv.imwrite("level_4.png", threshed)

    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle)
    '''
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