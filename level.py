import imutils
import numpy as np
import cv2 as cv
import glob

templates = ['level_1.png', 'level_2.png', 'level_3.png', 'level_4.png', 'collect.png']

level_fn = glob.glob("test_images/level*.png")

for level in level_fn:
    img = cv.imread(level, 0)

    crop_x, crop_y, crop_w, crop_h = 200, 120, 260, 235
    gray = img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    inverted = cv.bitwise_not(gray)
    ret,threshed = cv.threshold(inverted,60,255,cv.THRESH_BINARY) #30

    #crop_x, crop_y, crop_w, crop_h = 68, 140, 55, 32  #85, 28
    #threshed = threshed[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    #cv.imwrite("level_5.png", threshed)

    for t_name in templates:
        template = cv.imread(t_name,0)
        res = cv.matchTemplate(threshed,template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
        w, h = template.shape[::-1]
        #print(t_name, max_val)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        if max_val > 0.6:
            print("got it")
            break
    else:
        print("MISSED IT")
    #cv.imshow("Display window", threshed)
    #k = cv.waitKey(0)
