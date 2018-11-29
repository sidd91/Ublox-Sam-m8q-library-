# Library for Ublox GPS sensor and its application

## About

This repo involves reading the values from Ublox sam m8q gps sensor and provides multiple applications of the gps data e.g. geotagging

 
#### About the hardware

#### Files breakdown

readgpssensor.py reads the NMEA messages from the UART gps sensor

geotagging.py is a library of functions, facilitating applications such as embedding **gps exif data** in an image

main.py initializes the uart through read.py and embeds location in an image by using geotagging.py

#### Pinout NVIDIA TX2(to do)

### How to use?

python readgpssensor.py </dev/ttyTHS2> where /dev/ttyTHS2 is your serial device    

python main.py </dev/ttyTHS2>

python verify.py <image.jpg>


 
