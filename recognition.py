import imutils
import numpy as np
import cv2 as cv
import math
import time

DEBUG_VIDEO = False
cap = cv.VideoCapture(-1)

def flush_camera():
    for i in range(20):
        ret, frame = cap.read()
        
        
def get_template(letter): #load the template image and crop it.
    img = cv.imread('letters/'+letter+'.PNG', 0)
    ret,img = cv.threshold(img,200,255,cv.THRESH_BINARY)

    inverse = cv.bitwise_not(img)
    cnts, _ = cv.findContours(inverse, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv.boundingRect(c)[3] > 10]
    contour = cnts[0]
    bx, by, bw, bh = cv.boundingRect(contour)
    img = img[by:by+bh, bx:bx+bw]
    resized = cv.resize(img, (20, 25), interpolation = cv.INTER_AREA)
    return resized


letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_template_pairs = [(l, get_template(l)) for l in letters]



def piggy_bank():
    template = cv.imread('piggy_bank.png',0)
    ret, frame = cap.read()
    w, h = template.shape[::-1]

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    crop_x, crop_y, crop_w, crop_h = 190, 40, 200, 200
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    show_image(threshed)

    if max_val < 0.65:
        return None
    x, y = crop_x + top_left[0] + w, top_left[1] + crop_y
    return (x+20, y-15)

    
def next_level():
    templates = ['level_1.png', 'level_2.png', 'level_3.png', 'collect.png']
    ret, frame = cap.read()

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    crop_x, crop_y, crop_w, crop_h = 200, 120, 260, 235
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    inverted = cv.bitwise_not(gray)
    ret,threshed = cv.threshold(inverted,30,255,cv.THRESH_BINARY) #30
    show_image(threshed)
    for t_name in templates:
        template = cv.imread(t_name,0)
        res = cv.matchTemplate(threshed,template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
        w, h = template.shape[::-1]
        print(t_name, max_val)
        if max_val > 0.55:
            bottom_right = (top_left[0] + w, top_left[1] + h)
            return (crop_x+top_left[0]+(w/2), crop_y+top_left[1]+(h/2))


def get_circle_coord(img):
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=55,maxRadius=70) #param1 = 100
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
        if count > best_option_count:
            best_option = option
            best_option_count = count
    for l_and_l in attempts:
        letters = "".join([x[0] for x in l_and_l])
        if letters == best_option:
            return l_and_l
    


#fourcc = cv.VideoWriter_fourcc(*'MJPG')
#video_writer = cv.VideoWriter('video.mp4', fourcc, 20.0, (640,  480))
def record_video(frame=None):
    if not frame:
        ret, frame = cap.read()
    video_writer.write(frame)
    if cv.waitKey(1) == ord('q'):
        return


def can_have_three_letters():
    template = cv.imread('no_threes.png',0)
    ret, frame = cap.read()
    crop_x, crop_y, crop_w, crop_h = 175, 275, 130, 130
    frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    print("three letters max val", max_val)
    return max_val < 0.85 #we want this pretty high. We don't want to accidently match 

def get_letters_and_locations():
    ret, frame = cap.read()
    mask = cv.imread('mask_2.png',0)

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    coord = get_circle_coord(gray)
    try:    
        x, y, r = coord
        r = r-1
        crop_x, crop_y, crop_w, crop_h = x-r, y-r, r*2, r*2
        gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    except:
        show_image(gray)
        return None
    
    center, reach = crop_w // 2, crop_w // 5
    center_circle = gray[center-reach:center+reach, center-reach:center+reach]
    try:
        gray = cv.bilateralFilter(gray,5,75,75)
    except:
        return #we've cropped away the whole image.
    
    m = cv.mean(center_circle)[0]
    m2 = cv.mean(gray)[0]

    if m2 > m:
        gray = cv.bitwise_not(gray)
        center_color = 255-m
        ret,threshed = cv.threshold(gray, center_color,255,cv.THRESH_TRUNC)
        #ret,threshed = cv.threshold(threshed,center_color-20,255,cv.THRESH_BINARY) #I think the center color before was like 40, and this took it down to like 20.
        ret,threshed = cv.threshold(threshed,center_color*1/6,255,cv.THRESH_BINARY)
        #threshed = cv.adaptiveThreshold(threshed, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

    else:
        threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
        

    #show_image(threshed)

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
        if bh < 10: continue #too small
        if bw > 45 or bh > 30: continue # too big

        x, y = bx+(bw/2), by+(bh/2) #center of contour bounding box

        dx, dy = (crop_w/2)-x, (crop_h/2)-y
        dm = math.sqrt(dx * dx + dy * dy)
        
        if dm > (crop_w / 2) - 8 or dm < 35: #this filters out anything thats not on inside edge of the bounding circle. Replaces the mask
            continue

        location = (x+crop_x, y+crop_y)

        if bw < 6:
            game_letters.append(("I", location))
            continue        

        im = threshed[by:by+bh, bx:bx+bw]
        im = cv.resize(im, (20, 25), interpolation = cv.INTER_AREA)
     
        best_match = "A"
        best_score = 0
        A_template = None
        B_template = None
        for letter, letter_template in letter_template_pairs:
            if letter == "I" and bw > 7:
                continue
            if letter == "Z":
                A_template = letter_template
            if letter == "I":
                B_template = letter_template
            score = how_similar(im, letter_template)
            if score > best_score:
                best_score = score
                best_match = letter
        #if best_match == "Z":
        #    cv.imwrite("debug1.png", im)
        #    cv.imwrite("debug2.png", A_template)
        #    cv.imwrite("debug3.png", B_template)
        game_letters.append((best_match, location))
        if DEBUG_VIDEO:
            cv.rectangle(threshed,(bx, by), (bx+bw, by+bh), 0, 2) #make sure this is at the end.


    if DEBUG_VIDEO:
        show_image(threshed)
        print(game_letters)
        

    if len(game_letters) < 3:
        cv.imwrite("NoLetters.png", threshed)
        return None
    return game_letters


if __name__ == "__main__":
    DEBUG_VIDEO = True
    while True:        
        get_letters_and_locations()
