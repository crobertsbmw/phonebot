import serial
import time
from serial.tools import list_ports

def command(ser, command):
    ser.write(str.encode(command+"\n"))
    time.sleep(0.1)
    while True:
        line = ser.readline()
        print(line)
        if line == b'ok\n':
            break


ports = [str(p).split(" - ")[0] for p in list_ports.comports()]
print(ports)
baudrate = 115200

port = ports[0]

s = serial.Serial(port, baudrate)
time.sleep(2)
command(s, "M106 S0")
command(s, "M104 S0")
command(s, "M140 S0")
command(s, "G28")
command(s, "G90")
command(s, "G1 Z100 X100 Y100 F6000")
