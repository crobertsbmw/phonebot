import serial
import time
from serial.tools import list_ports

class PhoneBot:
    conn = None
    
    def command(self, command):
        self.conn.write(str.encode(command+"\n"))
        time.sleep(0.1)
        while True:
            line = self.conn.readline()
            print(line)
            if line == b'ok\n':
                break
    def connect(self):
        ports = [str(p).split(" - ")[0] for p in list_ports.comports()]
        print(ports)
        baudrate = 115200
        port = ports[0]
        self.conn = serial.Serial(port, baudrate)
        time.sleep(2.0)

    def home(self):
        self.command("M106 S0")
        self.command("M104 S0")
        self.command("M140 S0")
        self.command("G28")
        self.command("G90")

    def moveTo(self, x=None, y=None, z=None):
        cmd = "G1"
        if x != None:
            cmd += " X"+str(x)
        if y != None:
            cmd += " Y"+str(y)
        if z != None:
            cmd += " Z"+str(z)
        cmd += " F6000"
        self.command(cmd)


