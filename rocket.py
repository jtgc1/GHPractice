import cv2
import numpy as np
import math

#static pressure currently

h = 800
w = 1500
frame = np.zeros((h,w,3), np.uint8)
t = 0
oldDate = 'temp'

for i in range(10):
    for j in range(w):
        frame[h-1-i][j] = [0,255,0]

G = 6.647*10**-11
dt = 0.001
scalar = 1
g = 9.81

xc = 750*scalar
yc = 400*scalar

obj0 = [4.9*10**6, xc, 20, 0, 0, [255, 255, 255],20] #earth
obj1 = obj0
dm = 716*dt
FT = 74.5*10**6

def update():
    global obj0,g,FT,dm

    m = obj0[0]
    ax = 0
    ay = (-m*g + FT)/m

    dvx = ax * dt
    dvy = ay * dt
    obj0[3] = obj0[3] + dvx
    obj0[4] = obj0[4] + dvy
    dx = obj0[3] * dt
    dy = obj0[4] * dt

    colorFrame([0, 0, 0], obj0[1], obj0[2], obj1[6])

    obj1[1] = obj0[1] + dx
    obj1[2] = obj0[2] + dy
    obj1[0] = obj0[0] - dm

    colorFrame(obj0[5], obj1[1], obj1[2], obj1[6])

    print(obj0[0],obj0[2],obj0[4],ay)

    obj0 = obj1
def colorFrame(color,x,y,size):
    global frame,h,w,scalar
    xscaled = int(x//(scalar))
    yscaled = int(y//(scalar))

    sizeScaled = int(size//scalar)
    if sizeScaled == 0:
        sizeScaled = 1

    if sizeScaled%2 == 1:
        r = sizeScaled//2 + 1
    else:
        r = sizeScaled//2

    # print(xscaled,yscaled,sizeScaled)

    if yscaled < h and xscaled > 0:
        try:
            for i in range(r):
                l = int(math.sqrt(r**2-i**2))
                for j in range(l):
                    frame[h-yscaled+i][xscaled+j] = color
                    frame[h - yscaled - i][xscaled - j] = color
                    frame[h - yscaled + j][xscaled - i] = color
                    frame[h - yscaled - j][xscaled + i] = color
        except:
            pass

def displayTime():
    global t
    hours = (t//3600)
    days = (hours//24)
    months = (days//30)
    years = (days//365)
    hours = hours%24
    days = days%30
    months = months%12
    displayNumber(str(years)+','+str(months)+','+str(days)+','+str(hours))

def displayNumber(num):
    global oldDate
    x=3
    y = 4
    for j in range(2):
        x = 3
        if j == 0:
            w = [0,0,0]
            var = oldDate
        else:
            w = [255,255,255]
            var = num
            oldDate = num
        for i in str(var):
            if i == ',':
                frame[y+1][x] = w
                frame[y+2][x] = w
            if i == '0':
                frame[y-3][x-1] = w
                frame[y - 3][x] = w
                frame[y - 3][x+1] = w
                frame[y-2][x-2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x - 2] = w
                frame[y - 1][x + 2] = w
                frame[y][x - 2] = w
                frame[y][x + 2] = w
                frame[y+1][x - 2] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x+1] = w
            if i == '1':
                frame[y - 3][x] = w
                frame[y - 2][x - 1] = w
                frame[y - 2][x] = w
                frame[y - 1][x - 2] = w
                frame[y - 1][x] = w
                frame[y][x] = w
                frame[y + 1][x] = w
                frame[y + 2][x] = w
                frame[y + 3][x - 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
                frame[y + 3][x + 2] = w
            if i == '2':
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 2][x - 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x + 2] = w
                frame[y][x] = w
                frame[y][x + 1] = w
                frame[y + 1][x - 1] = w
                frame[y + 2][x - 2] = w
                frame[y + 3][x - 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
                frame[y + 3][x + 2] = w
            if i == '3':
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 2][x - 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x + 2] = w
                frame[y][x - 1] = w
                frame[y][x] = w
                frame[y][x + 1] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
            if i == '4':
                frame[y - 3][x + 1] = w
                frame[y - 2][x] = w
                frame[y - 2][x + 1] = w
                frame[y - 1][x - 1] = w
                frame[y - 1][x + 1] = w
                frame[y][x - 2] = w
                frame[y][x + 1] = w
                frame[y + 1][x - 2] = w
                frame[y + 1][x - 1] = w
                frame[y + 1][x] = w
                frame[y + 1][x + 1] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x + 1] = w
                frame[y + 3][x + 1] = w
            if i == '5':
                frame[y - 3][x - 2] = w
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 3][x + 2] = w
                frame[y - 2][x - 2] = w
                frame[y - 1][x - 2] = w
                frame[y - 1][x - 1] = w
                frame[y - 1][x] = w
                frame[y - 1][x + 1] = w
                frame[y][x + 2] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
            if i == '6':
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 2][x - 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x - 2] = w
                frame[y][x - 2] = w
                frame[y][x - 1] = w
                frame[y][x] = w
                frame[y][x + 1] = w
                frame[y + 1][x - 2] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
            if i == '7':
                frame[y - 3][x - 2] = w
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 3][x + 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x + 1] = w
                frame[y][x] = w
                frame[y + 1][x] = w
                frame[y + 2][x] = w
                frame[y + 3][x] = w
            if i == '8':
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 2][x - 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x - 2] = w
                frame[y - 1][x + 2] = w
                frame[y][x - 1] = w
                frame[y][x] = w
                frame[y][x + 1] = w
                frame[y + 1][x - 2] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
            if i == '9':
                frame[y - 3][x - 1] = w
                frame[y - 3][x] = w
                frame[y - 3][x + 1] = w
                frame[y - 2][x - 2] = w
                frame[y - 2][x + 2] = w
                frame[y - 1][x - 2] = w
                frame[y - 1][x + 2] = w
                frame[y][x - 1] = w
                frame[y][x] = w
                frame[y][x + 1] = w
                frame[y][x + 2] = w
                frame[y + 1][x - 2] = w
                frame[y + 1][x + 2] = w
                frame[y + 2][x - 2] = w
                frame[y + 2][x + 2] = w
                frame[y + 3][x - 1] = w
                frame[y + 3][x] = w
                frame[y + 3][x + 1] = w
            x = x + 6

while True:

    update()
    t = t + dt
    displayTime()
    # print(planetsOld[0][3], planetsOld[1][3], planetsOld[1][1])

    cv2.imshow('output', frame)

    if cv2.waitKey(1) == ord('q'):
        # press q to terminate the loop
        cv2.destroyAllWindows()
        break
