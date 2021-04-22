from recognition import get_letters_and_locations_20x, next_level, can_have_three_letters, record_video
from phonebot import PhoneBot
from dictionary import search_dictionary
from calibrator import camera_to_bot_coordinates
import time
import threading

bot = PhoneBot()
bot.connect()
bot.home()

can_video = False

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

def with_video(target, args):
    thread = threading.Thread(target=target, args=args)
    thread.start()
    while thread.isAlive():
        record_video()

def tap_out_word_with_video(word, landl):
    thread = threading.Thread(target=tap_out_word, args=(word,landl))
    thread.start()
    while thread.isAlive():
        record_video()


def move_to_with_video(x=None, y=None):
    thread = threading.Thread(target=bot.move_to, args=(x,y,None))
    thread.start()
    while thread.isAlive():
        record_video()


def tap_btn(location):
    bot.tap_up()
    x, y = camera_to_bot_coordinates(location)
    bot.move_to(x, y)
    bot.tap()

def tap_btn_with_video(location):
    thread = threading.Thread(target=tap_btn, args=(location,))
    thread.start()
    while thread.isAlive():
        record_video()

last_letters = []
remaining_words = []
while True:
    level = next_level()
    if level:
        print("Clicking next level")
        tap_btn_with_video(level)
        move_to_with_video(x = 50)

    three_letters = can_have_three_letters()
    letters_and_locations = get_letters_and_locations_20x()

    if not letters_and_locations:
        print("No Letters Found")
        continue

    letters = [l[0] for l in letters_and_locations]
    letters.sort()
    if remaining_words and last_letters == letters:
        words = remaining_words
    else:
        words = search_dictionary(letters, three_letters)
    last_letters = letters
    remaining_words = words[:]
    print(words)
    for word in words:
        print(word)
        tap_out_word(word, letters_and_locations)
        remaining_words.remove(word)
        if len(word) == len(letters):
            bot.move_to(x = 50)
            if not get_letters_and_locations_20x():
                break
    else:
        print("We got here because we failed to find a word. Here are the words we tried\n\n", words)
        move_to_with_video(x = 50)
    