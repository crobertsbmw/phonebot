import numpy as np
import cv2 as cv
import sys

cap = cv.VideoCapture(-1)
DEBUG_VIDEO = False

already_files = glob.glob("timelapse/*.png")
counts = [f.split("timelapse/")[1].split(".png")[0] for f in already_files]
counts = [int(f) for f in counts]
if not counts:
    counts = [0,]
count = max(counts) + 1

def get_gray():
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return gray

def save_timelapse():
    global count
    ret, frame = cap.read()
    cv.imwrite("timelapse/"+str(count)+".png", gray)
    count += 1

    
def show_image(img):
    if not DEBUG_VIDEO: return
    cv.imshow('image', img)
    if cv.waitKey(1) == ord('q'):
        return None