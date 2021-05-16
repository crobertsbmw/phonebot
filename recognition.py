import imutils
import numpy as np
import cv2 as cv
import math
import time
import glob
from dictionary import search_dictionary, search_backup_dictionary
DEBUG_VIDEO = False
cap = cv.VideoCapture(-1)
circle_mask = cv.imread('mask_2.png',0)

def get_all_combos(data):
    if len(data) == 0:
        return []
    if len(data) == 1:
        return [[x] for x in data[0]]
    combos = get_all_combos(data[1:])
    new_combos = []
    for letter in data[0]:
        new_combos = new_combos + [[letter]+combo for combo in combos]
    return new_combos

class Level():
    letters = []
    letters_scores = []
    attempts = 0
    center = None
    relax_constant = 10

    def equals(self, level):
        a = [x for x in self.letters if x not in level.letters]
        return len(a) < 2
        #return sorted(self.letters) == sorted(level.letters)

    def get_valid_letters_words_and_locations(self):
        print(self.attempts)
        three_letters = can_have_three_letters()
        letters = self.letters
        words = search_dictionary(letters, three_letters)
        if words and self.attempts == 0:
            if len(words) < 6:
                self.attempts += 1
            if len(words[-1]) != len(letters):
                words += search_backup_dictionary(letters, three_letters)
                words = list(set(words))
            return self.letters, words, self.locations
        elif self.attempts == 1 and words:
            return words, self.letters, self.locations
            
        all_availables = []
        #[[A:200, B:199], [A:200, B:199]]
        for score_chart in self.letters_scores:
            best_score = score_chart[0][0]
            print("Best Score", best_score)
            print("Score Chart", score_chart)
            availables = [x[1] for x in score_chart if x[0] > best_score-self.relax_constant]
            all_availables.append(availables)

        combos = get_all_combos(all_availables)

        other_valid_letters = []
        for potential in combos:
            trial_words = search_dictionary(potential, three_letters)
            trial_words = [x for x in trial_words if x not in words]
            if len(trial_words) > 1:
                other_valid_letters.append((potential, trial_words))

        i = self.attempts - 2
        if len(other_valid_letters) == 0:
            print("all our guesses are terrible")
            return None

        if i > len(other_valid_letters):
            return None

        i = self.attempts % len(other_valid_letters)
        letters, words, locations = other_valid_letters[i][0], other_valid_letters[i][1], self.locations
        print("returning other", words, len(other_valid_letters))
        return (letters, words, locations)



def flush_camera():
    for i in range(20):
        ret, frame = cap.read()
        
        
def get_template(filename): #load the template image and crop it.
    img = cv.imread(filename, 0)
    ret,img = cv.threshold(img,200,255,cv.THRESH_BINARY)

    inverse = cv.bitwise_not(img)
    cnts, _ = cv.findContours(inverse, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv.boundingRect(c)[3] > 10]
    contour = cnts[0]
    bx, by, bw, bh = cv.boundingRect(contour)
    img = img[by:by+bh, bx:bx+bw]
    resized = cv.resize(img, (20, 25), interpolation = cv.INTER_AREA)
    return resized


template_files = glob.glob("letters/*.PNG")
letter_template_pairs = []
for t in template_files:
    letter = t.split("letters/")[1][0]
    template = get_template(t)
    letter_template_pairs.append((letter, template))

def teams_thing():
    template = cv.imread('teams_screen.png',0)
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    return max_val > 0.75
    
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
    templates = ['level_1.png', 'level_2.png', 'level_3.png', 'level_4.png', 'collect.png']
    ret, frame = cap.read()

    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
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


last_circle_coord = None
def get_circle_coord(img):
    global last_circle_coord
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=55,maxRadius=70) #param1 = 100
    try:
        circles = np.uint16(np.around(circles))
    except:
        return last_circle_coord
    
    for i in circles[0,:]:
        last_circle_coord = i
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

#fourcc = cv.VideoWriter_fourcc(*'MJPG')
#video_writer = cv.VideoWriter('video.mp4', fourcc, 20.0, (640,  480))
def record_video(frame=None):
    if not frame:
        ret, frame = cap.read()
    video_writer.write(frame)
    if cv.waitKey(1) == ord('q'):
        return

def save_for_review(letters=None):
    ret, frame = cap.read()
    if not ret:
        print("no frame")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    import random
    n = random.randint(0,9999)
    if not letters:
        cv.imwrite("need_review/"+str(n)+".png", gray)
    else:
        cv.imwrite("need_review/"+letters+".png", gray)

def can_have_three_letters():
    template = cv.imread('no_threes.png',0)
    ret, frame = cap.read()
    crop_x, crop_y, crop_w, crop_h = 175, 275, 130, 130
    frame = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(gray,template,cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, top_left = cv.minMaxLoc(res)
    return max_val < 0.85 #we want this pretty high. We don't want to accidently match 

def get_center():
    x, y, r = last_circle_coord
    return (x,y)

def prepare_image(gray):
    for i in range(20):
        coord = get_circle_coord(gray)
    try:
        x, y, r = coord
        r = r-1
        crop_x, crop_y, crop_w, crop_h = x-r, y-r, r*2, r*2
        gray = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
    except:
        print("No Circle")
        show_image(gray)
        return None
    
    center, reach = crop_w // 2, crop_w // 5
    center_circle = gray[center-reach:center+reach, center-reach:center+reach]
    try:
        gray = cv.bilateralFilter(gray,5,75,75)
    except:
        print("Extra Crop")
        return #we've cropped away the whole image.
    
    m = cv.mean(center_circle)[0]
    m2 = cv.mean(gray)[0]

    inverted = cv.bitwise_not(gray)
    center_color = 255-m
    ret,threshed = cv.threshold(inverted, center_color,255,cv.THRESH_TRUNC)
    ret,threshed = cv.threshold(threshed,center_color*1/5,255,cv.THRESH_BINARY)

    threshed2 = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
    show_image(threshed)
    if m < m2: # flop flop threshed and threshed2
        t = threshed
        threshed = threshed2
        threshed2 = t

    mask = cv.resize(circle_mask, (r*2, r*2), interpolation = cv.INTER_AREA)
    try: #apply mask
        threshed = cv.bitwise_or(threshed, mask)
        threshed2 = cv.bitwise_or(threshed2, mask)
    except:
        return None    

    return threshed, threshed2, crop_x, crop_y

def get_letter_contours(inverted):
    h, w = inverted.shape
    all_contours, heirarchy = cv.findContours(inverted, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    letter_contours = []
    for contour in all_contours:
        bx, by, bw, bh = cv.boundingRect(contour)
        if bh < 10 or bh < 15: continue #too small
        if bw > 45 or bh > 30: continue # too big
        x, y = bx+(bw/2), by+(bh/2) #center of contour bounding box
        dx, dy = (w/2)-x, (h/2)-y
        dm = math.sqrt(dx * dx + dy * dy)
        if dm > (w / 2) - 8 or dm < 35: #this filters out anything thats not on inside edge of the bounding circle. Replaces the mask
            continue
        letter_contours.append(contour)
    return letter_contours


def get_level_data(frame=None, debug=False):
    if frame is None:
        ret, frame = cap.read()
        if not ret:
            print("no frame")
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    else:
        gray = frame
    data = prepare_image(gray)
    if not data:
        return
    threshed, threshed2, crop_x, crop_y = data
    inverted, inverted2 = cv.bitwise_not(threshed), cv.bitwise_not(threshed2)

    letter_contours = get_letter_contours(inverted)
    if len(letter_contours) < 4:
        letter_contours = get_letter_contours(inverted2)
        if len(letter_contours) < 4:
            return None
        else:
            print("SWAPPING FOR THRESHED 2 IMAGE")
            inverted = inverted2
            threshed = threshed2

    letters = []
    letters_scores = []
    locations = []
    imgs = []
    #TODO: Add a min threshold for the best_score so that we don't detect garbage as a letter.
    
    for contour in letter_contours:   
        bx, by, bw, bh = cv.boundingRect(contour) 
        x, y = bx+(bw/2), by+(bh/2) #center of contour bounding box
        location = (x+crop_x, y+crop_y)

        cropped = threshed[by:by+bh, bx:bx+bw]
        im = cv.resize(cropped, (20, 25), interpolation = cv.INTER_AREA)
        
        scores = []
        for letter, letter_template in letter_template_pairs:
            if letter == "I":
                if bw > 7:
                    score = 140
                else:
                    score = 230
            else:
                score = how_similar(im, letter_template)
            scores.append((score, letter))
        scores.sort()
        scores = scores[::-1]
        letters_scores.append(scores)
        locations.append(location)
        letters.append(scores[0][1])
        
        if DEBUG_VIDEO or debug:
            cv.rectangle(threshed,(bx-3, by-3), (bx+bw+3, by+bh+3), 150, 2) #make sure this is at the end.
    
    if debug:
        cv.imshow('image', threshed)
        k = cv.waitKey(0)
    if DEBUG_VIDEO:
        #show_image(threshed)
        print(letters)
 
    level = Level()
    level.letters = letters
    level.letters_scores = letters_scores
    level.locations = locations
    level.center = get_center()
    print(letters)
    return level



if __name__ == "__main__":
    DEBUG_VIDEO = True
    while True:        
        get_level_data()
