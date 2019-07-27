#!/usr/local/bin/python3

import os
import sys
from math import floor
from time import sleep

import cv2


beschriften = False
new_width = 800

# schrift
fontcolor = (0, 0, 0)
fontsize = 30
fps = 2 # Fotos pro Sekunde
#prefix1 = 'x'
prefix2 = 'y'

# movie
dir_path = r'A:\timelapse'
#dir_path = input('Pfad zu den Fotos: ')
ext = 'jpg'
# forcc = CV_FOURCC('M','J','P','G')
output = '_movie_' + str(fps) + 'fps.mp4'

# COUNTER
def counter(a,b):
    sys.stdout.write(str((a/b)*100)[:4] + '%') #f'\r{i}')
    sys.stdout.flush()
    # print(str((a/b)*100)[:4] + '%')


for file in os.listdir(dir_path):
    if file.endswith(ext):
        first_file = file
        break

image_path_first_file = os.path.join(dir_path, first_file)
frame = cv2.imread(image_path_first_file)
height, width, channels = frame.shape
imgScale = new_width/width
newWidth = int(width*imgScale)
newHeight = int(height*imgScale)
x = int(newWidth*0.05)
y = int(newHeight*0.9)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out_file = os.path.join(dir_path, output)
print('Datei:', out_file)
out = cv2.VideoWriter(out_file, fourcc, fps, (newWidth, newHeight))

images = []
for file in os.listdir(dir_path):
    if file.endswith(ext):
        # print(file)
        images.append(os.path.join(dir_path, file))

for n in range(10):
        images.append(images[-1])


n = len(images)
c = 0
frame_array = []
for image in images:
    # if file.endswith(ext):
        # print(image)
        img = cv2.imread(image, 1)
        c += 1
        if c % 2 == 0:
            counter(c,n)

        # fotos resizen
        img = cv2.resize(img, (newWidth, newHeight), interpolation = cv2.INTER_AREA)
        
        # fotos beschriften
        if beschriften:
            texts = image.split('\\')
            text = texts[-1].split('.')[0]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,text,(x, y), font, 0.6, (0,255,0),1,cv2.LINE_AA)

        # movie erstellen
        out.write(img)

out.release()

# TEMP files löschen
for file in os.listdir(dir_path):
    if file.startswith('NEW') and file.endswith(ext):
        os.remove(os.path.join(dir_path, file))
