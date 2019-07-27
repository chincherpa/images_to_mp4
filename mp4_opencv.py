#!/usr/local/bin/python3
import os
import sys
from math import floor
from time import sleep

import cv2
from progressbar import ProgressBar
from widgets import SimpleProgress, Percentage, Bar

bDREHEN = True

new_width = 10
##### schrift
bFOTOS_BESCHRIFTEN = False
fontcolor = (0, 0, 0)
fontsize = 30
##### video
fps = 10
# dir_path = input('Pfad zu den Fotos: ')
dir_path = r'C:\Users\x123069\Desktop\D\pys\images_to_mp4\images'
ext = 'png'
output = '0movie.mp4'

images = []
for file in os.listdir(dir_path):
    if file.endswith(ext):
        # print(file)
        images.append(os.path.join(dir_path, file))

image_path = images[0]
frame = cv2.imread(image_path)
height, width, channels = frame.shape
print('height, width, channels', height, width, channels)
center = (width / 2, height / 2)
print('center', center)
scale = 1.0

imgScale = new_width/width
newWidth = int(width*imgScale)
newHeight = int(height*imgScale)
x = int(newWidth*0.05)
y = int(newHeight*0.9)
print('imgScale, new_width, newWidth, newHeight', imgScale, new_width, newWidth, newHeight)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
out_file = os.path.join(dir_path, output)
out = cv2.VideoWriter(out_file, fourcc, fps, (newWidth, newHeight))

n = len(images)
c = 1
################################################################### Progressbar
#pbar = ProgressBar(widgets=[SimpleProgress()], maxval=n).start()
pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=n).start()

frame_array = []
for image in images:
#     print(c)
    pbar.update(c)
    img = cv2.imread(image, 1)

    # fotos resizen
    #img = cv2.resize(img, (newWidth, newHeight), interpolation = cv2.INTER_AREA)

############## drehen
    if bDREHEN:
        if c % 4 == 0:
            print('if c % 4 == 0:')
            # Perform the counter clockwise rotation holding at the center
            # 270 degrees
            M = cv2.getRotationMatrix2D(center, 270, scale)
            img = cv2.warpAffine(img, M, (height, width))
        elif c % 3 == 0:
            print('elif c % 3 == 0:')
            # Perform the counter clockwise rotation holding at the center
            # 180 degrees
            M = cv2.getRotationMatrix2D(center, 180, scale)
            img = cv2.warpAffine(img, M, (height, width))
        elif c % 2 == 0:
            print('elif c % 2 == 0:')
            # Perform the counter clockwise rotation holding at the center
            # 90 degrees
            M = cv2.getRotationMatrix2D(center, 90, scale)
            img = cv2.warpAffine(img, M, (height, width))

    # fotos beschriften
    if bFOTOS_BESCHRIFTEN:
        texts = image.split('\\')
        text = texts[-1].split('.')[0]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,text,(x, y), font, 0.6, (0,255,0),1,cv2.LINE_AA)

    cv2.imshow("Frames", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

#     sleep(0.2)
    # movie erstellen
    out.write(img)
    c += 1

out.release()
pbar.finish()
