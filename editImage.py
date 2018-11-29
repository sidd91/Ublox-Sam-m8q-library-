#https://gis.stackexchange.com/questions/136925/how-to-parse-exif-gps-information-to-lat-lng-decimal-numberis
import io 
from PIL import Image
import piexif
import read
import sys
import serial
from fractions import Fraction

im=Image.open("website.jpg")
#thumb_im.save(o,"jpeg")

def initialize_uart(dev):
    return read.init(dev)


def readgps(message):    
    if 'GNGGA' in message:
        return read.parseGGA(message)


def generate_exif_dict(gps_dict,lat_dms,long_dms):
    
    gps_ifd = {
    piexif.GPSIFD.GPSLatitudeRef:gps_dict['Lat_ref'],
    piexif.GPSIFD.GPSLatitude:((lat_dms['d'],1),(lat_dms['m'],1),(lat_dms['s'],1000)),
    piexif.GPSIFD.GPSLongitudeRef:gps_dict['Long_ref'],
    piexif.GPSIFD.GPSLongitude:((long_dms['d'],1),(long_dms['m'],1),(long_dms['s'],1))
    }
    exif_dict={"GPS":gps_ifd}
    return exif_dict

def degreetodms(degree):
    d=int(degree)
    m=int((degree-d)*60)
    s=float(degree-d-float(m)/60)*3600
    #s=float("{0:.3f}".format(s))
    print(d,m,s)
    return {'d':d,'m':m,'s':s}

def transform(gps_dict):
    
    gps_dict['Long'],gps_dict['Lat']= read.getlongandlat_in_degrees(gps_dict['Long'],gps_dict['Lat'])
    lat_dms=degreetodms(gps_dict['Lat'])
    long_dms=degreetodms(gps_dict['Long'])
    return lat_dms,long_dms      


def main():
    ser= initialize_uart(sys.argv[1])
    message = ""
    while('GNGGA' not in message):
        message = ser.readline()
        message=message.decode("utf-8",errors='ignore')
    print(message)
    gps_dict= readgps(message)
    lat_dms,long_dms=transform(gps_dict)
    exif_dict = generate_exif_dict(gps_dict,lat_dms,long_dms)
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes,"website.jpg")
    
main()

