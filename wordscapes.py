from phonebot import PhoneBot
from recognition import get_letters_and_locations, tear_down

bot = PhoneBot()
bot.connect()
bot.home()


while True:
    next_level = next_level():
    if next_level:
        tap_btn(next_level)

    sleep(2.0)

    three_letters = get_three_letters()
    letters_and_locations = get_letters_and_locations()

    if len(letters_and_locations < 0):
        print("No Letters Found")
        continue

    letters = [l[0] for l in letters_and_locations]
    words = get_all_words(letters, three_letters)

    for word in words:
        tap_out_word(words)
        sleep(1.0)
        if not get_letters_and_locations():
            break

def tap_btn(location):
    bot.tap_up()
    x, y = game_to_bot_coordinates(location)
    bot.move_to(x, y)
    bot.tap_down()
    sleep(0.15)
    bot.tap_up()

def game_to_bot_coordinates(location):
    #TODO: Figure this out.
    return
    x, y = location
    new_x = 600 + (x * 0.87)
    new_y = 300 + (y * 0.87)
    return new_x, new_y
    