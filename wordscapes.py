serial = connect_serial()
serial = home()

if start level:
    tap_next_level()
sleep(2.0)
three_letters = get_three_letters()
letters_and_locations = get_letters_and_locations()
letters = [l[0] for l in letters_and_locations]

words = get_all_words(letters, three_letters)

for word in words:
    tap_out_word(words)
    sleep(1.0)
    if not get_letters_and_locations():
        break

