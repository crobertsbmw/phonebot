import imutils
import numpy as np
import cv2 as cv
import math
import time

DEBUG_VIDEO = False

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
    #Fill this in.
    return True

def next_level():
    cap = cv.VideoCapture(-1)
    next_level_template = cv.imread('level_3.png',0)
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
        next_level_template = cv.imread('level_2.png',0)
        res = cv.matchTemplate(threshed,next_level_template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
        if max_val < 0.60:
            collect_template = cv.imread('collect.png',0)
            res = cv.matchTemplate(threshed,collect_template,cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
            w, h = collect_template.shape[::-1]
            if max_val < 0.60:
                return None
    
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #cv.rectangle(gray,top_left, bottom_right, 255, 2)
    
    return (crop_x+top_left[0]+(w/2), crop_y+top_left[1]+(h/2))


def get_circle_coord(img):
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=100,param2=30,minRadius=55,maxRadius=70)
    try:
        circles = np.uint16(np.around(circles))
    except:
        return None
    
    for i in circles[0,:]:
        #cv.circle(img,(i[0],i[1]),i[2]-10,(0,255,0),2)
        #cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
        return i

def show_image(img):
    if not DEBUG_VIDEO: return
    cv.imshow('image', img)
    if cv.waitKey(1) == ord('q'):
        return None

def how_similar(img1, img2):
    img = cv.bitwise_xor(img1, img2)
    m = cv.mean(img)[0]
    return 255-m

def get_letters_and_locations_20x():
    attempts = [get_letters_and_locations() for x in range(20)]
    attempts = [x for x in attempts if x]
    if len(attempts) < 2:
        return None
    attempts = [sorted(x, key=lambda x:x[0]) for x in attempts]
    letters = ["".join([x[0] for x in attempt]) for attempt in attempts]
    
    options = list(set(letters))
    best_option, best_option_count = options[0], 0
    for option in options:
        count = letters.count(option)
        print(option, count)
        if count > best_option_count:
            best_option = option
            best_option_count = count
    for l_and_l in attempts:
        letters = "".join([x[0] for x in l_and_l])
        if letters == best_option:
            return l_and_l

def record_video():
    cap = cv.VideoCapture(-1)
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    out = cv.VideoWriter('video.mp4', fourcc, 20.0, (640,  480))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # write the flipped frame
        out.write(frame)
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    out.release()
    cv.destroyAllWindows()
    
def get_letters_and_locations():
    cap = cv.VideoCapture(-1)
    ret, frame = cap.read()
    cap.release()
    #mask = cv.imread('mask_2.png',0)

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    coord = get_circle_coord(gray)
    
    gray = cv.bilateralFilter(gray,7,75,75)
    
    try:    
        x, y, r = coord
        r = r-1
        crop_x, crop_y, crop_w, crop_h = x-r, y-r, r*2, r*2
        gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    except:
        show_image(gray)
        return None

    
    m = cv.mean(gray)[0]
    if m < 160:
        gray = cv.bitwise_not(gray)
        ret,threshed = cv.threshold(gray,25,255,cv.THRESH_BINARY)
    else:
        threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
   

    #show_image(threshed)
    show_image(threshed)

    #mask = cv.resize(mask, (r*2, r*2), interpolation = cv.INTER_AREA)
    #threshed = cv.bitwise_or(threshed, mask)

    inverted = cv.bitwise_not(threshed)

    cnts, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    contours = [c for c in cnts if cv.boundingRect(c)[3] > 15]
    
    game_letters = []
    
    #TODO: Add a min threshold for the best_score so that we don't detect garbage as a letter.
    for contour in contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        if bh < 18: continue #too small
        if bw > 45 or bh > 30: continue # too big

        x, y = bx+(bw/2), by+(bh/2) #center of contour bounding box

        dx, dy = (crop_w/2)-x, (crop_h/2)-y
        dm = math.sqrt(dx * dx + dy * dy)
        
        if dm > (crop_w / 2) - 8 or dm < 35: #this filters out anything thats not on inside edge of the bounding circle. Replaces the mask
            continue
                        
        im = threshed[by:by+bh, bx:bx+bw]
        im = cv.resize(im, (50, 50), interpolation = cv.INTER_AREA)
     
        best_match = "A"
        best_score = 0
        for letter, letter_template in letter_template_pairs:
            #template matching
            #res = cv.matchTemplate(im,letter_template,cv.TM_CCORR_NORMED)
            #score = res[0][0]
            score = how_similar(im, letter_template)
            if score > best_score:
                best_score = score
                best_match = letter
        location = (x+crop_x, y+crop_y)
        #if best_score > 0.40:
        game_letters.append((best_match, location))
        #elif bw/bh < 5/22 and bw/bh > 1/22: #possibly an I
        #    area = cv.contourArea(contour)
        #    rect_area = bw*bh
        #    extent = float(area)/rect_area
        #    if extent > 0.35:
        #        game_letters.append(("I", location))
        #else:
        #    print("Can't figure out what the letter is..")
        if DEBUG_VIDEO:
            cv.rectangle(threshed,(bx, by), (bx+bw, by+bh), 0, 2) #make sure this is at the end.


    if DEBUG_VIDEO:
        print(game_letters)
        

    if len(game_letters) < 3:
        print("WRITE NO LETTERS")
        cv.imwrite("NoLetters.png", threshed)
        return None
    return game_letters


if __name__ == "__main__":
    DEBUG_VIDEO = True
    while True:        
        record_video()
