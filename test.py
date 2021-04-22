import time
import threading

busy = False

def run_bot_stuff(word):
    print("starting bot", word)
    time.sleep(3.0)
    print("finished bot", word)
    global busy
    busy = False

word = "Hello"
busy = True
thread = threading.Thread(target=run_bot_stuff, args=(word,))  
thread.start()

while True:
    print("Capture Video")
    time.sleep(0.1)
    if not busy:
        break

print("done done done")
