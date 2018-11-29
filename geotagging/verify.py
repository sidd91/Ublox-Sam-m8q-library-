import piexif
import geocoder
from decimal import *


API_KEY= 'UwKcPqj3bzhx3USXvFRHA9GsTkO9hWWa'

def findplace(Lat, Long):
    g=geocoder.mapquest([Lat,Long], method='reverse' , key= API_KEY)
    print("Place= ", g)

def dmstodegree(_tuple,ref):
    d=_tuple[0][0]
    m=_tuple[1][0]
    s=float(Decimal(_tuple[2][0])/Decimal(_tuple[2][1])) 
    
    #print("s=",float(s))
    dd=float(d) + float(Decimal(m)/Decimal(60)) + float(s/3600)
    print(s)
    
    if ref == "S" or ref == 'W':
        dd = -1 * float(dd)
  
    return dd
   









def main():
    exif_dict=piexif.load("website.jpg")
    GPS_dict=exif_dict['GPS']        
    lat=dmstodegree(GPS_dict[2],GPS_dict[1])
    longitude=dmstodegree(GPS_dict[4],GPS_dict[3])
    print(lat, longitude)
    findplace(lat,longitude)


main()


