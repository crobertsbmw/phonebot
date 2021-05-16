from recognition import *
from phonebot import PhoneBot
from dictionary import search_dictionary, search_backup_dictionary, sort_words_20x
from calibrator import camera_to_bot_coordinates
import time, random
import cv2 as cv

bot = PhoneBot()
bot.connect()
bot.home()


# def save_letters():
#     imgs = get_letters_and_locations(return_imgs=True)
#     for image, letter in imgs:
#         n = random.randint(0,9999)
#         cv.imwrite("letters/needs_assignment_"+letter+str(n)+".PNG", image)

def tap_out_word(word, letters, locations, center=None):
    letters = letters[:]
    locations = locations[:]
    #first_letter = True
    bot.tap_up()
    if center:
        cx, cy = camera_to_bot_coordinates(center)
    
    for i, letter in enumerate(word):
        for l, location in zip(letters, locations):
            if l == letter:
                x, y = camera_to_bot_coordinates(location)
                bot.move_to(x=x, y=y)
                if i == 0:
                    bot.tap_down()
                    first_letter = False
                locations.remove(location)
                letters.remove(l)
                if center and i != len(word)-1: #recenter between words so we don't accidently pick up exra letters.
                    bot.move_to(x=cx, y=cy)
                break
    bot.tap_up()


def tap_btn(location):
    bot.tap_up()
    x, y = camera_to_bot_coordinates(location)
    bot.move_to(x, y)
    bot.tap()


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


last_tap = 0
can_save_for_review = False
last_level = None
while True:
    last_tap += 1
    flush_camera()
    if last_tap == 25:
        print("Last Tap is too High. Saving image...")
        save_for_review()
        break
    
    next_level_btn = next_level()        
    if next_level_btn:
        finding_word_attempts = 0
        can_save_for_review = True
        tap_btn(next_level_btn)
        last_tap = 0
        bot.move_to(x = 200)
        time.sleep(0.5)
    elif teams_thing():
        finding_word_attempts = 0
        bot.move_to(x=112, y=250)
        bot.tap()

    level = get_level_data()
    if not level:
        continue

    if last_level and level.equals(last_level):
        level = last_level
    
    d = level.get_valid_letters_words_and_locations()
    if not d:
        relax = level.relax_constant
        level = get_level_data()
        level.relax_constant = relax + 5
        #shuffle and try again
        if can_save_for_review:
            can_save_for_review = False
            save_for_review()
        time.sleep(0.5)
        continue
    
    letters, words, locations = d
    words = sort_words_20x(words, len(letters))
    print(words)

    if level.attempts > 0:
        center = get_center()
    else:
        center = None
    
    level.attempts += 1
    last_level = level
    x_btn = piggy_bank()
    if x_btn:
        print("click piggy bank")
        tap_btn(x_btn)
    
    for i, word in enumerate(words):
        tap_out_word(word, letters, locations, center)

    bot.move_to(x=200)
    time.sleep(2.5)
