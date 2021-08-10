import numpy as np
import cv2 as cv
import sys
import glob

cap = cv.VideoCapture(-1)
DEBUG_VIDEO = False

already_files = glob.glob("timelapse/*.png")
counts = [f.split("timelapse/")[1].split(".png")[0] for f in already_files]
counts = [int(f) for f in counts]
if not counts:
    counts = [0,]
lapse_count = max(counts) + 1

next_level_files = glob.glob("next_level_lapse/*.png")
counts = [f.split("next_level_lapse/")[1].split(".png")[0] for f in next_level_files]
counts = [int(f) for f in counts]
if not counts:
    counts = [0,]
next_level_count = max(counts) + 1

def get_gray():
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return gray

def save_timelapse():
    global lapse_count
    for i in range(0,20):
        ret, frame = cap.read()
    cv.imwrite("timelapse/"+str(lapse_count)+".png", frame)
    lapse_count += 1

def next_level_lapse():
    global next_level_count
    ret, frame = cap.read()
    cv.imwrite("next_level_lapse/"+str(next_level_count)+".png", frame)
    next_level_count += 1

    
def show_image(img):
    if not DEBUG_VIDEO: return
    cv.imshow('image', img)
    if cv.waitKey(1) == ord('q'):
        return None