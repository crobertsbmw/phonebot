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
    
