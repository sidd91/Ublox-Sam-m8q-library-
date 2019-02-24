#Author: Siddharth Chawla
#Revision: v0.0 
#About: Python script to verify the location embed in the .jpg file(website.jpg here)

import piexif
import geocoder
from decimal import *
from mapbox import StaticStyle
import sys
import os

map_quest_API_KEY= '<Add token>'    #Enter Mapquest API key
map_box_access_token = "<Add Token>" #Enter Mapbox API key
directory = 'final_image'
service = StaticStyle(access_token = map_box_access_token)

lat = 0.0
lon = 0.0
name = ""

feature = []

#create at most 100 dictionary variables which will have the json enteries 
temp_feature = [dict() for x in range(100)]

#decodes the lat and long to a readable address
def findplace(Lat, Long):
    g=geocoder.mapquest([Lat,Long], method='reverse' , key=map_quest_API_KEY)
    print("Place= ", g)

def dmstodegree(_tuple,ref):
    d=_tuple[0][0]
    m=_tuple[1][0]
    s=float(Decimal(_tuple[2][0])/Decimal(_tuple[2][1])) 
    dd=float(d) + float(Decimal(m)/Decimal(60)) + float(s/3600)

    if ref == "S" or ref == 'W':
        dd = -1 * float(dd)
  
    return dd


# create a feature dictionary for every location image location we got
def get_feature(lat, lon, name):

    val = {
        'type' : 'Feature',
        'properties': {'name':'SJSU','marker-symbol':'waste-basket'},
        'geometry':{
            'type': 'Point',
            'coordinates':[lon, lat]
        }}
    return val
 

def main():
    i = 0

    #reads all the file in the directory and will only read upto 100 files, this is because of the limitation of the overlays in mapbox	
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') and i<100:
            filename = os.path.join(directory,filename) 
            exif_dict = piexif.load(filename)
            GPS_dict = exif_dict['GPS']
            lat=dmstodegree(GPS_dict[2],GPS_dict[1])
            longitude=dmstodegree(GPS_dict[4],GPS_dict[3])
            name = findplace(lat,longitude)
            temp_feature[i] = get_feature(lat, longitude, name)
            i+=1 
 #populate a final feature list - it is used to overlay in the mapbox api
    for x in temp_feature:
        if x:
            feature.append(x)
    
    print(type(feature), type(feature[0]))
    response = service.image(username = 'mapbox', style_id = 'streets-v9',features = feature)
    print(response.status_code)
    
    with open('map.png','wb') as output:
        _= output.write(response.content)

     
main()
