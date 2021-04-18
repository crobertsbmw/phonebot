import numpy as np
import cv2 as cv
import imutils

cap = cv.VideoCapture(-1)

def get_template(letter): #load the template image and crop it.
    img = cv.imread('letters/'+letter+'.PNG', 0)
    ret,img = cv.threshold(img,200,255,cv.THRESH_BINARY)

    inverse = cv.bitwise_not(img)
    cnts, _ = cv.findContours(inverse, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv.boundingRect(c)[3] > 10]
    contour = cnts[0]
    bx, by, bw, bh = cv.boundingRect(contour)
    img = img[by:by+bh, bx:bx+bw]
    resized = cv.resize(img, (50, 50), interpolation = cv.INTER_AREA)
    return resized


letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_template_pairs = [(l, get_template(l)) for l in letters]


    
while True:
    mask = cv.imread('mask_2.png',0)
    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray = cv.bilateralFilter(gray,7,75,75)
    # gray = cv.GaussianBlur(gray,(5,5),0)
    #cv.imshow('image2', gray)
    #crop_x, crop_y, crop_w, crop_h = 255, 245, 125, 125
    #gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.bilateralFilter(gray,7,75,75)
    cimg = cv.cvtColor(gray,cv.COLOR_GRAY2BGR)

    circles = cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,20,
                                param1=100,param2=30,minRadius=55,maxRadius=70)
    print("unrounded", circles)
    circles = np.uint16(np.around(circles))
    print("around", circles)
    print()
    for i in circles[0,:]:
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    

    cv.imshow('image', cimg)
    if cv.waitKey(1) == ord('q'):
        break


def tear_down():
    cap.release()
    cv.destroyAllWindows()
