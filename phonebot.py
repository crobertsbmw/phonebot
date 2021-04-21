import serial
import time
from serial.tools import list_ports
Z_UP = 6
Z_DOWN = 1
class PhoneBot:
    conn = None
    
    def command(self, command):
        self.conn.write(str.encode(command+"\n"))
        while True:
            line = self.conn.readline()
            if line == b'ok\n':
                break
            print("BOT", line)


    def connect(self):
        ports = [str(p).split(" - ")[0] for p in list_ports.comports()]
        print(ports)
        baudrate = 115200
        port = ports[0]
        self.conn = serial.Serial(port, baudrate)
        time.sleep(2.0)

    def home(self):
        self.command("M107")
        self.command("M104 S0")
        self.command("M140 S0")
        self.command("G28")
        self.command("G90")
        self.command("G0 Y150 F7000")
        self.command("G0 Z6")
        self.command("M400")

    def move_to(self, x=None, y=None, z=None):
        if y and y < 120:
            print("ERROR. Y CANNOT BE LESS THAN 120")
            return
        cmd = "G1"
        if x != None:
            cmd += " X"+str(x)
        if y != None:
            cmd += " Y"+str(y)
        if z != None:
            cmd += " Z"+str(z)
        cmd += " F7000"
        self.command(cmd)
        self.command("M400")
        self.command("M107")

    def tap_down(self):
        self.move_to(z=Z_DOWN)

    def tap_up(self):
        self.move_to(z=Z_UP)

    def tap(self):
        self.tap_down()
        self.tap_up()

