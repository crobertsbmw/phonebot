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

def can_have_three_letters():
    template = cv.imread('level.png',0)
    ret, frame = cap.read()
    crop_x, crop_y, crop_w, crop_h = 175, 275, 130, 130
    frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    return max_val > 0.7 

def next_level():
    template = cv.imread('level.png',0)
    w, h = template.shape[::-1]

    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)

    if max_val < 0.80: 
        return None
    return (top_left[0]+(w/2), top_left[1]+(h/2))

    
while True:
    mask = cv.imread('mask_2.png',0)
    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray = cv.bilateralFilter(gray,7,75,75)
    # gray = cv.GaussianBlur(gray,(5,5),0)
    cv.imshow('image2', gray)

    crop_x, crop_y, crop_w, crop_h = 255, 235, 125, 125
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.bilateralFilter(gray,7,75,75)
    m = cv.mean(gray)[0]
    if m < 160:
        gray = cv.bitwise_not(gray)

    threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    #threshed = cv.bitwise_or(threshed, mask)

    inverted = cv.bitwise_not(threshed)
    cnts, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    contours = [c for c in cnts if cv.boundingRect(c)[3] > 15]
    
    game_letters = []

    #TODO: Add a min threshold for the best_score so that we don't detect garbage as a letter.
    print("****")
    for contour in contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        if bh < 15: continue #too small
        if bw > 50 or bh > 50: continue # too big
        print(bw, bh)
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
        if best_score > 0.45:
            location = (bx+(bw/2), by+(bh/2))
            game_letters.append((best_match, location))

    print(game_letters)

    cv.imshow('image', threshed)
    if cv.waitKey(1) == ord('q'):
        break


def tear_down():
    cap.release()
    cv.destroyAllWindows()
