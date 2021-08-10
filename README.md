# BRUTE - The Wordscapes Dominating Robot

[![Wordscapes Dominating Robot](https://i.imgur.com/to0U2ay.png)](https://www.youtube.com/watch?v=R-qC-0gX8Dw "Wordscapes Dominating Robot")


Sending Commands to the Robot
-----------------------------
Then I think the only depency here is pyserial
```
pip install pyserial
```

First connect a USB cable to your 3d printer. If you're using an Ender 3 it's the micro usb cable port in the front.
With any luck, you can then just import the phonebot.py file and call:

```
from phonebot import PhoneBot

bot = PhoneBot()
bot.connect()
bot.home()
```
Don't be a fraid to dig into the phonebot.py file. It's pretty straightforward, and you might need to make some edits depending on what you are trying to do.


Doing Everything Else
---------------------

I'm assuming everyone just wants the bit for moving the robot around. But if you want to replicate the entire project, then I've included all the other files as well.
The kickoff point for everything is the wordscapes.py file. You should start there.
