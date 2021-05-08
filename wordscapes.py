from recognition import get_letters_and_locations_20x, next_level, can_have_three_letters, piggy_bank, flush_camera
from phonebot import PhoneBot
from dictionary import search_dictionary, search_backup_dictionary, sort_words_20x
from calibrator import camera_to_bot_coordinates
import time

bot = PhoneBot()
bot.connect()
bot.home()

'''
subpar, blog, merlot, techno, ebook, cooktop, chemo
'''

def tap_out_word(word, landl):
    landl = landl[:]
    first_letter = True
    bot.tap_up()
    for letter in word:
        for i, v in enumerate(landl):
            l, location = v
            if l == letter:
                x, y = camera_to_bot_coordinates(location)
                bot.move_to(x=x, y=y)
                if first_letter:
                    bot.tap_down()
                    first_letter = False
                landl.remove(v)
                break
    bot.tap_up()


def tap_btn(location):
    bot.tap_up()
    x, y = camera_to_bot_coordinates(location)
    bot.move_to(x, y)
    bot.tap()

last_letters = []
repeat_count = 0
while True:
    flush_camera()
    level = next_level()
    if level:
        print("Clicking next level")
        tap_btn(level)
        bot.move_to(x = 200)

    letters_and_locations_list = get_letters_and_locations_20x()
    if not letters_and_locations_list:
        print("No Letters Found")
        continue

    for letters_and_locations in letters_and_locations_list: #Make sure that you can make an N letter word with the letters that came back.
        letters = [l[0] for l in letters_and_locations]
        words = search_dictionary(letters)
        if words and len(words[-1]) == len(letters):
            if last_letters == letters and repeat_count > 3:
                print("We've already tried this three times. Let's try some other letters?")
                continue
            break
    else:
        print("Valid Letters Not Found.")
        continue

    three_letters = can_have_three_letters()

    x_btn = piggy_bank()
    if x_btn:
        print("click piggy bank")
        tap_btn(x_btn)
    
    print("letters", letters)
    words = search_dictionary(letters, three_letters)
    #words = brute_force(letters, "C****")

    if last_letters == letters:
        print("Adding backup words")
        repeat_count+=1
        words += search_backup_dictionary(letters)
        words = list(set(words))
    else:
        repeat_count = 0
    
    last_letters = letters
    if len(words) < 6:
        continue
    words = sort_words_20x(words, len(letters))
    print(words)
    
    for i, word in enumerate(words):
        print(word)
        tap_out_word(word, letters_and_locations)
        #if repeat_count > 0 and i % 5 == 0:
        #    bot.move_to(x=200)
        #    if not get_letters_and_locations_20x():
        #        print("I think we figured it out")
        #        break
    bot.move_to(x=200)
    time.sleep(2.5)
