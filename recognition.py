import imutils
import numpy as np
import cv2 as cv
import time
from cam import *

DEBUG_VIDEO = False

def teams_thing():
    template = cv.imread('teams_screen.png',0)
    gray = get_gray()
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    return max_val > 0.6
    
def piggy_bank():
    template = cv.imread('piggy_bank.png',0)
    w, h = template.shape[::-1]

    gray = get_gray()
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
    templates = ['level_1.png', 'level_2.png', 'level_3.png', 'level_4.png', 'collect.png']
    gray = get_gray()
    
    crop_x, crop_y, crop_w, crop_h = 200, 120, 260, 235
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    inverted = cv.bitwise_not(gray)
    ret,threshed1 = cv.threshold(inverted,30,255,cv.THRESH_BINARY)
    ret,threshed2 = cv.threshold(inverted,60,255,cv.THRESH_BINARY)
    show_image(threshed1)
    for threshed in [threshed1, threshed2]:
        for t_name in templates:
            template = cv.imread(t_name,0)
            res = cv.matchTemplate(threshed,template,cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
            w, h = template.shape[::-1]
            if max_val > 0.6:
                bottom_right = (top_left[0] + w, top_left[1] + h)
                return (crop_x+top_left[0]+(w/2), crop_y+top_left[1]+(h/2))


def how_similar(img1, img2):
    img = cv.bitwise_xor(img1, img2)
    m = cv.mean(img)[0]
    return 255-m

#fourcc = cv.VideoWriter_fourcc(*'MJPG')
#video_writer = cv.VideoWriter('video.mp4', fourcc, 20.0, (640,  480))
def record_video(frame=None):
    if not frame:
        frame = get_gray()
    video_writer.write(frame)
    if cv.waitKey(1) == ord('q'):
        return

def save_for_review(letters=None):
    gray = get_gray()
    import random
    n = random.randint(0,9999)
    if not letters:
        cv.imwrite("need_review/"+str(n)+".png", gray)
    else:
        cv.imwrite("need_review/"+letters+".png", gray)

def can_have_three_letters():
    template = cv.imread('no_threes.png',0)
    gray = get_gray()
    crop_x, crop_y, crop_w, crop_h = 175, 275, 130, 130
    gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    return max_val < 0.85 #we want this pretty high. We don't want to accidently match 
