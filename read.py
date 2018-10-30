 #!/usr/bin/env python
          
      
import time
import serial

#GGA=0
#time=1
#lattitude=2
#Lattitude_dir=3


def parse_GNGGA(GNGGA):
    pass
    
ser = serial.Serial(
   
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
counter=0


while 1:
    x=ser.readline()
    list_GNGGA=''
    list_G=[]
    if '$GNGGA' in x:
        list_GNGGA=x
        for x in list_GNGGA.split(','):
            list_G.append(x)
        print(list_G)
