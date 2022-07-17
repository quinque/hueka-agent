#!/usr/bin/python3

latitude = "49.0165"
longitude = "8.3825"
description = "Mischa Treppenhaus"

from io import BytesIO
from time import sleep
from datetime import datetime
from picamera import PiCamera
from picamera import Color
from PIL import Image
import math 
import numpy as np

from numpy import interp
from numpy import clip
from subprocess import call
#json post
import requests

### uv sensor import and config
import board
import adafruit_ltr390
from adafruit_ltr390 import LTR390, MeasurementDelay, Resolution, Gain
i2c = board.I2C()
ltr = adafruit_ltr390.LTR390(i2c)
ltr.resolution = Resolution.RESOLUTION_20BIT
ltr.gain = Gain.GAIN_9X
#clip 900000 interp 6,25 with gain9
###


camera = PiCamera(resolution=(1920, 1080),  framerate=4)
camera.iso = 100
#camera.exposure_compensation = 5
#camera.brightness = 70
#camera.contrast = -10
camera.saturation = 0
sleep(5)
camera.exposure_mode = 'auto'

camera.awb_mode = 'off'
#white balance set, red, blue 
#camera.awb_gains = (1.58, 1.66)
camera.awb_gains = (1.60, 1.66)
# zoom in the middle
#camera.zoom = (0.4, 0.3, 0.2, 0.2)
count = 0

def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

while True:
    count += 1
    #capture image as PIL stream
    stream = BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    image = Image.open(stream)

    e = camera.exposure_speed
    e = 1000000/e
    # print('exposure_speed: ', e)



    imgarray = np.mean(image, axis=(0, 1))
    # round the rgb values, then convert to int
    # imgarray = np.around(imgarray)
    # imgarray = imgarray.astype(int)
    hlscolor = Color.from_rgb_bytes(imgarray[0], imgarray[1], imgarray[2]).hls
    naivecolor = Color.from_rgb_bytes(imgarray[0], imgarray[1], imgarray[2])
    # print('hls: ', hlscolor)


     
    lightness = clip(ltr.light, 1, 900000)
    # print("Ambient Light:", lightness)
    #lightness = math.log10(lightness)
    lightness = math.log(lightness) / math.log(30)
    # print("log10 Ambient Light:", lightness)
    lightness = interp(lightness,[1,5],[0,1])
    # print("Mapped Ambient Light:", lightness)
    #saturation lower when light lower
    # saturation = hlscolor[2] + (lightness - 0.65)/2
    # saturation = clip(saturation, 0, 1)
    # print("hls color:", hlscolor[0], lightness, saturation)
    # rgbcolor = Color.from_hls(hlscolor[0], lightness, saturation).rgb_bytes
    # print("hls color:", hlscolor[0], lightness, hlscolor[2])
    rgbcolor = Color.from_hls(hlscolor[0], lightness, hlscolor[2]).rgb_bytes
    rgbhex = Color.from_hls(hlscolor[0], lightness, hlscolor[2])
    # print("RGB Color:", rgbcolor )
    # print("Naive: ", imgarray)

    #image.paste( hlscolor, [0,0,image.size[0],image.size[1]])
    naive = Image.new(mode="RGB", size=(1,200), color=(int(imgarray[0]), int(imgarray[1]), int(imgarray[2])))
    naive = naive.save("now_naive.png","PNG")
    loglightness = Image.new(mode="RGB", size=(1,200), color=rgbcolor)
    loglightness = loglightness.save("now_loglightness.png","PNG")
    image = image.resize((1, 200), Image.LANCZOS)
    image = image.save("now_photo.png","PNG")
    rc = call("./append.sh", shell=True)


   

    timestamp = datetime.now()
    
    skydata=(timestamp.isoformat() + ", " + str(naivecolor) + ", " + str(ltr.light) + ", " + str(rgbhex) + ", " + str(latitude) + ", " + str(longitude) + ", " + str(description) )
    print(skydata)

    year = '{:02d}'.format(timestamp.year)
    month = '{:02d}'.format(timestamp.month)
    day = '{:02d}'.format(timestamp.day)
    day_month_year = '{}-{}-{}'.format(year, month, day)

    append_new_line('skyrecords/' + day_month_year + '/' + day_month_year + '_data.txt', skydata)
    
    try:
        response = requests.post("https://api.himmelueberkarlsruhe.de/", json={"timestamp":timestamp.isoformat(), "naivecolor":str(naivecolor), "light":ltr.light, "rgbhex":str(rgbhex), "latitude":latitude, "longitude":longitude, "description":description}, timeout=7)
        print("Status code: ", response.status_code)
        print(response.json())
    except Exception:
        print("ERROR in posting data.")
        pass

    stream.close()
    sleep(17) 


#for filename in camera.capture_continuous('img{counter:03d}.jpg'):
    # e = camera.exposure_speed
    # e = 1000000/e
    # e = clip(e, 1, 8000)
    # ef = math.log10(e)
    # ef = clip(ef, 0.7, 3.6)
    # ex = interp(ef,[3,15],[50,70])
    # ex = int(ex)


#    #between 0 and 100
#    camera.brightness = ex
#    print('brightness' , ex)
    # print('exposure_speed', e)
    # print('log2 light value' , ef)
    # print('Captured %s' % filename)
    # print(imgarray)
    # print("Ambient Light:", ltr.light)
    # sleep(20) 