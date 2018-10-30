import serial 
from time import sleep
port=serial.Serial("/dev/serial1")

while True:
    port.write("Say Something")
    sleep(0.5)
