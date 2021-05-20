from recognition import *
from level import *
from cam import save_timelapse
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

def tap_out_moves(moves, center=None):
    bot.tap_up()
    if center:
        cx, cy = camera_to_bot_coordinates(center)
    
    for j, move_set in enumerate(moves):
        for i, move in enumerate(move_set):
            x, y = camera_to_bot_coordinates(move)
            bot.move_to(x=x, y=y)
            if i == 0:
                bot.tap_down()
            if center and i != len(move_set)-1: #recenter between words so we don't accidently pick up exra letters.
                bot.move_to(x=cx, y=cy)
        if j % 4 == 0:
            save_timelapse()
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

def shuffle():
    bot.move_to(x=117, y=160)
    bot.tap()
    bot.move_to(x = 95)

last_tap = 0
can_save_for_review = False
last_level = None
relaxed = False
level_btn_loc = None
blind_next_level = False
while True:
    last_tap += 1
    flush_camera()
    if last_tap == 20:
        print("Last Tap is too High. Saving image...")
        save_for_review()
        break
    
    next_level_btn = next_level()        
    if next_level_btn:
        print("***************Next Level***************")
        level_btn_loc = next_level_btn
        finding_word_attempts = 0
        shuffles = 0
        relaxed = False
        can_save_for_review = True
        last_tap = 0
        tap_btn(next_level_btn)
        bot.move_to(x = 200)
        time.sleep(0.5)
    elif teams_thing():
        finding_word_attempts = 0
        bot.move_to(x=115, y=230)
        bot.tap()
    
    level = get_level_data()
    if not level:
        if level_btn_loc and last_tap > 0 and last_tap % 5 == 0:
            print("tapping next level button that we couldn't detect.")
            tap_btn(level_btn_loc)
            blind_next_level = True
            bot.move_to(x = 95)
            time.sleep(0.5)
        continue
    elif relaxed:
        level.relax_constant = 20

    if last_level and level.equals(last_level):
        level = last_level
    
    moves = level.get_moves()
    if not moves:
        relaxed = True
        print("SHUFFLING")
        shuffle()
        level = None
        last_level = None
        if can_save_for_review:
            can_save_for_review = False
            save_for_review()
        time.sleep(0.5)
        continue
    
    if blind_next_level:
        blind_next_level = False
        last_tap = 0
    
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
    
    tap_out_moves(moves, center)

    bot.move_to(x=200)
    save_timelapse()
    time.sleep(2.5)
