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

def getlongandlat_in_degrees(Long,Lat):
    

    dd= int(float(Lat)/100)
    ss=float(Lat)-float(dd*100)
    Lat=dd+ss/60 
    Lat=float("{0:.7f}".format(Lat))
    #calculation for latitude
    ddd= int(float(Long)/100)
    ss=float(Long)-ddd*100
    Long=ddd+ss/60
    Long=float("{0:.7f}".format(Long))
    print("read,py",Lat, Long) 
    return (Long,Lat)
    

def parselatandlong(Long, Long_dir, Lat, Lat_dir):
    '''Lattitude format is in ddss.sssss '''
    dd= int(float(Lat)/100)
    ss=float(Lat)-float(dd*100)
    Lat=dd+ss/60
    print(dd,ss,Lat)
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
        #print("Lat= ",Lat,"and Long= ", Long)
        print("Number of satellites", GGA[GGAEnum.numberofsatellites.value])
        #Lat, Long= parselatandlong(Long, Long_dir, Lat, Lat_dir)
        return {'Long':Long,'Long_ref':Long_dir,'Lat':Lat, 'Lat_ref':Lat_dir}
        #findplace(Lat, Long)
        #findplace(37.331149, -121.874717) 

def findplace(Lat, Long):
    g=geocoder.mapquest([Lat,Long], method='reverse' , key= API_KEY)
    print("Place= ", g)


def init(dev):
    '''initializes the UART, default dev= /dev/ttyTHS2 and baud rate =9600'''
    device_file = sys.argv[1]
    ser = serial.Serial(
    port=device_file,
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
    return ser

ser= init(sys.argv[1])

def main():
    while 1:
      x=ser.readline()
      #print(x)
      x= x.decode("utf-8",errors='ignore')
      if 'GNGGA' in x:
        parseGGA(x)



