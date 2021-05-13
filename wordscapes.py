from recognition import get_letters_and_locations, get_letters_and_locations_20x, next_level, can_have_three_letters, piggy_bank, flush_camera, save_for_review, get_center, teams_thing
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
    landl = landl[:]
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
                landl.remove(v)
                if center and i != len(word)-1: #recenter between words so we don't accidently pick up exra letters.
                    bot.move_to(x=cx, y=cy)
                break
    bot.tap_up()


def tap_btn(location):
    bot.tap_up()
    x, y = camera_to_bot_coordinates(location)
    bot.move_to(x, y)
    bot.tap()


def get_all_combos(l1, l2):
    if len(l1) == 1:
        return [l1, l2]
    combos = get_all_combos(l1[1:], l2[1:])
    print(combos)
    combos = [[l1[0]]+c for c in combos] + [[l2[0]]+c for c in combos]
    return combos



def get_valid_letters_words_and_locations(attempt=0):
    letters, backup_letters, locations = get_letters_and_locations()
    if not letters:
        return None, None, None

    three_letters = can_have_three_letters()
    words = search_dictionary(letters, three_letters)
    
    if attempt > 0: #look for more words
        words += search_backup_dictionary(letters)
        words = list(set(words))
    if words and len(words[-1]) == len(letters) and attempt < 2:
        return letters, words, locations #This handles most cases.

    #If we get here, it's because we can't make a six letter word with the standard letters.
    combos = get_all_combos(letters, backup_letters)

    other_valid_letters = []
    for potential in combos:
        words = search_dictionary(potential, three_letters)
        if words and len(words[-1]) == len(letters):
            other_valid_letters.append(potential, words)

    if attempt == 1: attempt = 0
    elif attempt > 2: attempt -= 0

    if attempt > len(other_valid_letters) * 2:
        print("I think we have to give up.")
        return None, None, None

    i = attempt % len(other_valid_letters)
    letters, words, locations = other_valid_letters[attempt][0], other_valid_letters[attempt][1], locations        

    return letters, words, locations





last_tap = 0
finding_letter_attempts = 0
while True:
    last_tap += 1
    flush_camera()
    level = next_level()
    if last_tap == 25:
        print("Last Tap is too High. Saving image...")
        save_for_review()
        
    if level:
        finding_letter_attempts = 0
        tap_btn(level)
        last_tap = 0
        bot.move_to(x = 200)
    elif teams_thing():
        bot.move_to(x=112, y=250)
        bot.tap()

    letters, words, locations = get_valid_letters_words_and_locations(finding_letter_attempts)
    if not words:
        finding_letter_attempts += 1
        if finding_letter_attempts == 1:
            save_for_review()
        time.sleep(0.5)
        continue

    words = sort_words_20x(words, len(letters))
    print(words)

    if finding_letter_attempts > 0:
        center = get_center()
    else:
        center = None
    
    x_btn = piggy_bank()
    if x_btn:
        print("click piggy bank")
        tap_btn(x_btn)
    
    for i, word in enumerate(words):
        print(word)
        tap_out_word(word, letters, locations, center)
       
    last_tap = 0
    bot.move_to(x=200)
    time.sleep(2.5)
