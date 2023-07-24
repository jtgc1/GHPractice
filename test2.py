import cv2
import numpy as np
import math

#make it startable from a specific point in real time
#make it scrollable
#switch to a pre calculated option and then simulate it once the math is done

#make a rocket ship that leaves the earth's atmosphere
#regressive path finding algorithm?
#trip ends if they get to the location or go past the raial distance of the location or go past the sun

h = 800
w = 1500
frame = np.zeros((h,w,3), np.uint8)
t = 0
oldDate = 'temp'
scalar = 1

def colorFrame(color,x,y,size):
    global frame,h,w,scalar,h
    xscaled = int(x//(scalar))
    yscaled = int(y//(scalar))

    sizeScaled = int(size//scalar)
    if sizeScaled == 0:
        sizeScaled = 1

    r = sizeScaled//2

    pi = math.pi

    # print(size, xscaled,yscaled)
    if yscaled < h and xscaled > 0:
        try:
            for j in range(r):
                c = math.sqrt(r**2 - j**2)
                l = int(c)
                for i in range(l):
                    frame[h-y+j][x+i] = color
                    frame[h-y-j][x-i] = color
                    frame[h-y+i][x-j] = color
                    frame[h-y-i][x+j] = color
        except:
            pass

colorFrame([255,255,255],w//2,h//2,300)

cv2.imshow('output', frame)
cv2.waitKey(0)
