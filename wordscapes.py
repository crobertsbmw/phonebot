from recognition import get_letters_and_locations_20x, next_level, can_have_three_letters, piggy_bank, flush_camera
from phonebot import PhoneBot
from dictionary import search_dictionary, search_backup_dictionary, sort_words_20x
from calibrator import camera_to_bot_coordinates
import time

bot = PhoneBot()
bot.connect()
bot.home()

'''
subpar, blog, merlot, techno, ebook, cooktop
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
while True:
    flush_camera()
    level = next_level()
    if level:
        print("Clicking next level")
        tap_btn(level)
        bot.move_to(x = 200)

    letters_and_locations = get_letters_and_locations_20x()
    three_letters = can_have_three_letters()

    x_btn = piggy_bank()
    if x_btn:
        print("click piggy bank")
        tap_btn(x_btn)
        
    if not letters_and_locations:
        print("No Letters Found")
        continue

    letters = [l[0] for l in letters_and_locations]
    print("letters", letters)
    words = search_dictionary(letters, three_letters)
    if last_letters == letters:
        print("Adding backup words")
        words += search_backup_dictionary(letters)
        words = list(set(words))        
        
    last_letters = letters
    if len(words) < 6:
        continue
    words = sort_words_20x(words, len(letters))
    print(words)
    
    for word in words:
        print(word)
        tap_out_word(word, letters_and_locations)
        #if len(word) == len(letters):
        #    bot.move_to(x = 50)
        #    if not get_letters_and_locations_20x():
        #        break
    bot.move_to(x=200)
    time.sleep(2.5)