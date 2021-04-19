import numpy as np
import cv2 as cv
import imutils

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
debug = 0

def can_have_three_letters():
    #Fill this in.
    return True

def next_level():
    cap = cv.VideoCapture(-1)
    global debug
    debug += 1
    next_level_template = cv.imread('level_3.png',0)
    collect_template = cv.imread('collect.png',0)


    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    crop_x, crop_y, crop_w, crop_h = 200, 120, 260, 235
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    inverted = cv.bitwise_not(gray)
    ret,threshed = cv.threshold(inverted,30,255,cv.THRESH_BINARY)

    res = cv.matchTemplate(threshed,next_level_template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    w, h = next_level_template.shape[::-1]

    if max_val < 0.60:
        res = cv.matchTemplate(threshed,collect_template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
        w, h = collect_template.shape[::-1]

        if max_val < 0.60:
            return None
    
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(gray,top_left, bottom_right, 255, 2)
    cv.imwrite("next_level_"+str(debug)+".png", gray)

    return (crop_x+top_left[0]+(w/2), crop_y+top_left[1]+(h/2))


def get_circle_coord(img):
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=100,param2=30,minRadius=55,maxRadius=70)
    try:
        circles = np.uint16(np.around(circles))
    except:
        return None

    for i in circles[0,:]:
        # draw the outer circle
        return i

def show_image(img):
    cv.imshow('image', img)
    if cv.waitKey(1) == ord('q'):
        return None

def get_letters_and_locations(video=False, cap=None):
    if not cap:    
        cap = cv.VideoCapture(-1)
        ret, frame = cap.read()
        cap.release()
    else:
        ret, frame = cap.read()

    mask = cv.imread('mask_2.png',0)

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.bilateralFilter(gray,7,75,75)

    coord = get_circle_coord(gray)
    try:    
        x, y, r = coord
        crop_x, crop_y, crop_w, crop_h = x-r, y-r, r*2, r*2
        gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    except:
        if video:
            show_image(gray)
        return None


    m = cv.mean(gray)[0]
    if m < 160:
        gray = cv.bitwise_not(gray)

    threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

    mask = cv.resize(mask, (r*2, r*2), interpolation = cv.INTER_AREA)
    threshed = cv.bitwise_or(threshed, mask)

    inverted = cv.bitwise_not(threshed)
    cnts, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    contours = [c for c in cnts if cv.boundingRect(c)[3] > 15]
    
    game_letters = []

    #TODO: Add a min threshold for the best_score so that we don't detect garbage as a letter.
    for contour in contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        if bh < 15: continue #too small
        if bw > 50 or bh > 50: continue # too big

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
            location = (bx+(bw/2)+crop_x, by+(bh/2)+crop_y)
            game_letters.append((best_match, location))
    if video:
        show_image(threshed)
        print(game_letters)
        

    if len(game_letters) < 3:
        return None
    return game_letters


if __name__ == "__main__":
    cap = cv.VideoCapture(-1)
    while True:
        get_letters_and_locations(video=True, cap=cap)
