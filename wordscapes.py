from phonebot import PhoneBot
from recognition import get_letters_and_locations, next_level, can_have_three_letters
from dictionary import search_dictionary
from calibrator import camera_to_bot_coordinates
import time

bot = PhoneBot()
bot.connect()
bot.home()


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
    
while True:
    level = next_level()
    if level:
        print("Clicking next level")
        tap_btn(level)
        bot.move_to(x = 100)

    time.sleep(2.5)

    three_letters = can_have_three_letters()
    letters_and_locations = get_letters_and_locations()

    if not letters_and_locations or len(letters_and_locations) < 2:
        print("No Letters Found")
        continue

    letters = [l[0] for l in letters_and_locations]
    print(letters)
    words = search_dictionary(letters, three_letters)
    print(words)
    for word in words:
        print(word)
        tap_out_word(word, letters_and_locations)
        if len(word) == len(letters):
            bot.move_to(x = 100)
            if not get_letters_and_locations():
                break
    else:
        print("We got here because we failed to find a word. Here are the words we tried\n\n", words)
        bot.move_to(x = 100)
    