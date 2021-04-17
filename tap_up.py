from phonebot import PhoneBot
from recognition import get_letters_and_locations, next_level, can_have_three_letters
from dictionary import search_dictionary
import time

bot = PhoneBot()
bot.connect()
bot.tap_up()
bot.move_to(x=0)