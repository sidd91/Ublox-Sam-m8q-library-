import time
import serial
import datetime
import geocoder
from enum import Enum
import sys
import os


GGA=[]
#LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
API_KEY= 'UwKcPqj3bzhx3USXvFRHA9GsTkO9hWWa'

class GGAEnum(Enum):
    UTCtime=1
    Lat=2
    Lat_dir=3
    Long=4
    Long_dir=5
    Fixquality=6
    numberofsatellites=7

def utctocurrent_tmzone(LOCAL_TIMEZONE):
    pass

def parselatandlong(Long, Long_dir, Lat, Lat_dir):
    '''Lattitude format is in ddss.sssss '''
    dd= int(float(Lat)/100)
    ss=float(Lat)-float(dd*100)
    Lat=dd+ss/60

    #calculation for latitude
    ddd= int(float(Long)/100)
    ss=float(Long)-ddd*100
    Long=ddd+ss/60

    if Lat_dir == "S":
        Lat = -1 * float(Lat)

    if Long_dir == "W":
        Long = -1 * float(Long)

    return Lat, Long

def parseGGA(inputGGA):
    GGA=inputGGA.split(",")
    if GGA[GGAEnum.Fixquality.value]==0:   
        print("Invalid Data")
    else:
        Long     = GGA[GGAEnum.Long.value]
        Long_dir = GGA[GGAEnum.Long_dir.value]
        Lat      = GGA[GGAEnum.Lat.value]
        Lat_dir  = GGA[GGAEnum.Lat_dir.value]
        Lat, Long= parselatandlong(Long, Long_dir, Lat, Lat_dir)
        print("Lat= ",Lat,"and Long= ", Long)
        print("Number of satellites", GGA[GGAEnum.numberofsatellites.value])
        findplace(Lat, Long)
        #findplace(37.331149, -121.874717) 

def findplace(Lat, Long):
    g=geocoder.mapquest([Lat,Long], method='reverse' , key= API_KEY)
    print("Place= ", g)

device_file = sys.argv[1]
ser = serial.Serial(
   
    port=device_file,
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


while 1:
    #os.system("sudo cat " + device_file)
    x=ser.readline()
    print(x)
    x= x.decode("utf-8",errors='ignore')
    if 'GNGGA' in x:
        pass
        #parseGGA(x)



