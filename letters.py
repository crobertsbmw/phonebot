import imutils
import numpy as np
import cv2 as cv
import glob
from recognition import get_letters_and_locations


templates = ['level_1.png', 'level_2.png', 'level_3.png', 'level_4.png', 'collect.png']

level = glob.glob("test_images/level*.png")
collect = glob.glob("test_images/collect*.png")
letter_filenames = glob.glob("test_images/*.png")
#letter_filenames = glob.glob("test_images/mum*.png")

letter_filenames = [x for x in letter_filenames if x not in level]
letter_filenames = [x for x in letter_filenames if x not in collect]
letter_filenames.sort()

#for file_name in letter_filenames:
#    img = cv.imread(file_name, 0)
#    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
#                                param1=10,param2=30,minRadius=55,maxRadius=70) #param1 = 100
#    try:
#        circles = np.uint16(np.around(circles))
#    except:
#        print("No Circle")
#        cv.imshow("Display window", img)
#        k = cv.waitKey(0)
#        continue
#    for i in circles[0,:]:
#        cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
#        cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
#    cv.imshow("Display window", img)
#    k = cv.waitKey(0)

'''
file_name = "test_images/team_thing_1.png"
img = cv.imread(file_name, 0)
crop_x, crop_y, crop_w, crop_h = 210, 0, 205, 380
img = img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
cv.imwrite("teams_screen.png", img)
cv.imshow("Display window", img)
k = cv.waitKey(0)
'''
'''
cap = cv.VideoCapture(-1)
template = cv.imread('teams_screen.png',0)
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    print("three letters max val", max_val)
    print("top left", top_left)
    cv.imshow('image', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
'''
'''
import random

for file_name in letter_filenames:
    img = cv.imread(file_name, 0)
    imgs = get_letters_and_locations(img, return_imgs=True)
    for image in imgs:
        n = random.randint(0,9999)
        cv.imwrite("letters/needs_assignment_"+str(n)+".PNG", image)
'''

for file_name in letter_filenames:
    img = cv.imread(file_name, 0)
    landl = get_letters_and_locations(img, debug=False)
    if not landl:
        print("Not Found", file_name)
    
    actual_letters = file_name.split("images/")[1].split("_")[0].upper()
    actual_letters = [x for x in actual_letters]
    letters = [x[0] for x in landl]
    for l in letters:
        if l in actual_letters:
            actual_letters.remove(l)
        else:
            print("WRONG LETTER -", l)
            print(file_name, letters)
            landl = get_letters_and_locations(img, debug=True)
            break
    else:
        if actual_letters:
            print("FAILED TO DETECT -", actual_letters)
        else:
            print("PASSED", file_name)
