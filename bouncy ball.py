import cv2
import numpy as np

h = w = 600
frame = np.zeros((h,w), np.uint8)
g = -9.81
x = y = h//2
xint = x
yint = y
frame[h-y][w-x] = 255
vx = vy = 20
t = 0
dt = 0.01

def upPos():
    global x,y,vy,vx,dt,frame,t,xint,yint
    frame[h-yint][xint] = 0
    dvx = 0
    dvy = g*dt
    vx = vx + dvx
    vy = vy + dvy

    dx = vx*dt
    dy = vy*dt
    x = x + dx
    y = y + dy

    t = t + dt
    if y <= 0:
        vy = -vy
        y = abs(y)
    if y <= 1:
        vy = -vy
        y = 1
    if x <= 0:
        vx = -vx
        x = abs(x)
    if x >= w:
        vx = -vx
        x = 2*w -x

    xint = int(x)
    yint = int(y)
    # print(x, y)
    # print(xint, yint)
    frame[h-yint][xint] = 255



while True:

    upPos()

    cv2.imshow('output', frame)

    if cv2.waitKey(10) == ord('q'):
        # press q to terminate the loop
        cv2.destroyAllWindows()
        break