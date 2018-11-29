#Author:Siddharth Chawla
#Revision: v0
#About: This file calls read.py and geotagging.py which initializes the uart interface for the UBlox SAM-M8Q GPS sensor and embeds location in .jpg files 



import io 
from PIL import Image
import piexif
import read
import sys
import serial
import geotagging as gt


def main():
    ser= gt.initialize_uart(sys.argv[1])
    message = ""
    while('GNGGA' not in message):
        message = ser.readline()
        message=message.decode("utf-8",errors='ignore')
    print(message)
    gps_dict= gt.readgps(message)
    lat_dms,long_dms=gt.transform(gps_dict)
    exif_dict = gt.generate_exif_dict(gps_dict,lat_dms,long_dms)
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes,"website.jpg")
    #print(piexif.load("website.jpg"))  
    #print(exif_dict)


main()
