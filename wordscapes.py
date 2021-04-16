from phonebot import PhoneBot
from recognition import get_letters_and_locations, next_level, tear_down, can_have_three_letters
from dictionary import search_dictionary
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

def camera_to_bot_coordinates(location):
    bot_min_x = 112
    bot_bottom_y = 129
    bot_max_x = 180
    bot_top_y = 230
    cam_min_x = 215
    cam_max_x = 425
    cam_top_y = 82
    cam_bottom_y = 390
    x, y = location
    new_x = (x-cam_min_x) / (cam_max_x-cam_min_x) * (bot_max_x-bot_min_x) + bot_min_x
    new_y = (y-cam_bottom_y) / (cam_top_y-cam_bottom_y) * (bot_top_y-bot_bottom_y) + bot_bottom_y
    return new_x, new_y
    
print("KICKING OFF")
while True:
    level = next_level()
    if level:
        print("Clicking next level")
        tap_btn(level)

    time.sleep(2.0)

    three_letters = can_have_three_letters()
    letters_and_locations = get_letters_and_locations()

    if not letters_and_locations or len(letters_and_locations) < 2:
        print("No Letters Found")
        continue

    letters = [l[0] for l in letters_and_locations]
    words = search_dictionary(letters, three_letters)

    for word in words:
        tap_out_word(word, letters_and_locations)
        time.sleep(0.5)
        if len(word) == len(letters):
            bot.move_to(x = 100)
            if not get_letters_and_locations():
                break
    else:
        print("We got here because we failed to find a word. Here are the words we tried\n\n", words)
    