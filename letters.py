import random
import imutils
import numpy as np
import cv2 as cv
import glob
from recognition import get_letters_and_locations, get_circle_coord


templates = ['level_1.png', 'level_2.png', 'level_3.png', 'level_4.png', 'collect.png']

level = glob.glob("test_images/level*.png")
collect = glob.glob("test_images/collect*.png")
letter_filenames = glob.glob("need_review/*.png")
#letter_filenames = glob.glob("test_images/mum*.png")

letter_filenames = [x for x in letter_filenames if x not in level]
letter_filenames = [x for x in letter_filenames if x not in collect]
letter_filenames.sort()

def test_circles():
    for file_name in letter_filenames:
       img = cv.imread(file_name, 0)
       circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                   param1=10,param2=30,minRadius=55,maxRadius=70) #param1 = 100
       try:
           circles = np.uint16(np.around(circles))
       except:
           print("No Circle")
           cv.imshow("Display window", img)
           k = cv.waitKey(0)
           continue
       for i in circles[0,:]:
           cv.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
           cv.circle(img,(i[0],i[1]),2,(0,0,255),3)
       cv.imshow("Display window", img)
       k = cv.waitKey(0)
    
def test_teams_screen():
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


def show(img):
    return
    resized = cv.resize(img, (200, 250), interpolation = cv.INTER_AREA)
    cv.imshow('image', resized)
    k = cv.waitKey(0)

def test_templates():
    file_names = glob.glob("letters/*.PNG")
    file_names = [x for x in file_names if len(x) < 14]
    
    file_names.sort()
    print(file_names)
    for filename in file_names:
        letter = filename.split("/")[1][0].upper()
        img = cv.imread(filename, 0)
        ret,img = cv.threshold(img,200,255,cv.THRESH_BINARY)
        show(img)

        kernel = np.ones((3,3),np.uint8)
        #img = cv.erode(img,kernel,iterations = 1)
        img = cv.dilate(img,kernel,iterations = 1)
        show(img)

        inverse = cv.bitwise_not(img)

        show(inverse)

        cnts, _ = cv.findContours(inverse, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = [c for c in cnts if cv.boundingRect(c)[3] > 10]
        contour = cnts[0]
        bx, by, bw, bh = cv.boundingRect(contour)
        img = img[by:by+bh, bx:bx+bw]
        print("printing", letter)
        cv.imwrite("letters/"+letter+"_C.PNG", img)
        show(img)
        
def save_letters(file_name):
    file_name = glob.glob("test_images/"+file_name+"*.png")[0]
    img = cv.imread(file_name, 0)
    imgs = get_letters_and_locations(img, return_imgs=True)
    for image, l in imgs:
        n = random.randint(0,9999)
        cv.imwrite("letters/needs_assignment_"+l+str(n)+".PNG", image)
  

def test_letters():
    for file_name in letter_filenames:
        img = cv.imread(file_name, 0)
        letters, backup_letters, locations = get_letters_and_locations(img, debug=False)
        if not letters:
            print("Not Found", file_name)
        
        actual_letters = file_name.split("/")[1].split("_")[0].split(".")[0].upper()
        actual_letters = [x for x in actual_letters]
        for l in letters:
            if l in actual_letters:
                actual_letters.remove(l)
            else:
                print("WRONG LETTER -", l)
                print(file_name, letters)
                _ = get_letters_and_locations(img, debug=True)
                break
        else:
            if actual_letters:
                print("FAILED TO DETECT -", actual_letters)
            else:
                print("PASSED", file_name)
#test_templates()
test_letters()
#save_letters("sqt")