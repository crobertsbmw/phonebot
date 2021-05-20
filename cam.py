import numpy as np
import cv2 as cv
import sys

cap = cv.VideoCapture(-1)
DEBUG_VIDEO = False

def get_gray():
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return gray

    
def show_image(img):
    if not DEBUG_VIDEO: return
    cv.imshow('image', img)
    if cv.waitKey(1) == ord('q'):
        return None