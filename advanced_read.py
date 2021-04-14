import numpy as np
import cv2 as cv
import imutils

cap = cv.VideoCapture(-1)
mask = cv.imread('mask_2.png',0)

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
    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray = cv.bilateralFilter(gray,7,75,75)
    # gray = cv.GaussianBlur(gray,(5,5),0)

    crop_x, crop_y, crop_w, crop_h = 255, 185, 125, 125
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]


    threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

    threshed = cv.bitwise_or(threshed, mask)

    inverted = cv.bitwise_not(threshed)
    cnts, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    contours = [c for c in cnts if cv.boundingRect(c)[3] > 10]
    for i, c in enumerate(contours):
        bx, by, bw, bh = cv.boundingRect(c)
        #cv.rectangle(threshed, (bx, by), (bx+bw, by+bh), (0,0,255), 2)
        #cv.drawContours(gray, [c], -1, (0,0,255), 2)
    
    game_letters = []
    for contour in contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        im = threshed[by:by+bh, bx:bx+bw]
        im = cv.resize(im, (50, 50), interpolation = cv.INTER_AREA)
        best_match = "A"
        best_score = 0
        for letter, letter_template in letter_template_pairs:
            #template matching
            res = cv.matchTemplate(im,letter_template,cv.TM_CCOEFF_NORMED)
            score = res[0][0]
            if score > best_score:

                best_score = score
                best_match = letter
        game_letters.append(best_match)

    print(game_letters)

    #cv.imwrite("tatcr.png", gray)

    cv.imshow('frame', threshed)
    if cv.waitKey(1) == ord('q'):
        break


cap.release()
cv.destroyAllWindows()



print(pytesseract.image_to_string(Image.open('tatcr.png')))