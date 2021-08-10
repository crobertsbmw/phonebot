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

def how_similar(img1, img2):
    img = cv.bitwise_xor(img1, img2)
    m = cv.mean(img)[0]
    return 255-m

fourcc = cv.VideoWriter_fourcc(*'MJPG')
video_writer = cv.VideoWriter('video.mp4', fourcc, 20.0, (640,  480))

def record_video(frame=None):
    video_writer.write(frame)
    cv.imshow('image', frame)
    if cv.waitKey(1) == ord('q'):
        return


def get_letters_and_locations():
    ret, frame = cap.read()
    mask = cv.imread('mask_2.png',0)

    if not ret:
        print("no frame")
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    coord = get_circle_coord(gray)
    
    gray = cv.bilateralFilter(gray,5,75,75)
    v_frame = cv.cvtColor(gray,cv.COLOR_GRAY2RGB) 
    
    try:    
        x, y, r = coord
        r = r-1
        crop_x, crop_y, crop_w, crop_h = x-r, y-r, r*2, r*2
        gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    except:
        return
    
    center, reach = crop_w // 2, crop_w // 5
    center_circle = gray[center-reach:center+reach, center-reach:center+reach]

    m = cv.mean(center_circle)[0]
    m2 = cv.mean(gray)[0]

    if m2 > m:
        gray = cv.bitwise_not(gray)
        v_frame = cv.bitwise_not(v_frame)

        center_color = 255-m
        print(center_color)
        ret,threshed = cv.threshold(gray, center_color,255,cv.THRESH_TRUNC)
        ret,v_frame = cv.threshold(v_frame, center_color,255,cv.THRESH_TRUNC)
        #ret,threshed = cv.threshold(threshed,center_color-20,255,cv.THRESH_BINARY) #I think the center color before was like 40, and this took it down to like 20.
        ret,threshed = cv.threshold(threshed,center_color*2/8,255,cv.THRESH_BINARY)
        ret,v_frame = cv.threshold(v_frame,center_color*2/8,255,cv.THRESH_BINARY)

        #threshed = cv.adaptiveThreshold(threshed, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

    else:
        threshed = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
        


    mask = cv.resize(mask, (r*2, r*2), interpolation = cv.INTER_AREA)
    threshed = cv.bitwise_or(threshed, mask)

    inverted = cv.bitwise_not(threshed)
    v_frame = cv.bitwise_not(v_frame)
    cnts, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    
    cv.circle(v_frame,(x,y),r, (0,0,255), 2)

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
        im = cv.resize(im, (20, 25), interpolation = cv.INTER_AREA)
     
        best_match = "A"
        best_score = 0
        for letter, letter_template in letter_template_pairs:
            #template matching
            #res = cv.matchTemplate(im,letter_template,cv.TM_CCORR_NORMED)
            #score = res[0][0]
            if letter == "I" and bw > 7:
                continue
            score = how_similar(im, letter_template)
            if score > best_score:
                best_score = score
                best_match = letter
        location = (x+crop_x, y+crop_y)
        game_letters.append((best_match, location))
        cv.rectangle(v_frame,(bx+crop_x, by+crop_y), (bx+bw+crop_x, by+bh+crop_y), (0,255,0), 2)
    letters = [l[0] for l in game_letters]
    locations = [l[1] for l in game_letters]
    print(" ".join(letters),"  ", locations)
    record_video(v_frame)


if __name__ == "__main__":
    DEBUG_VIDEO = True
    while True:        
        get_letters_and_locations()

