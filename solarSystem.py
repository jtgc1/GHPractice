import cv2
import numpy as np

#make it startable from a specific point in real time

h = 800
w = 1500
frame = np.zeros((h,w,3), np.uint8)

G = 6.647*10**-11
dt = 86400*4
scalar = 6.3*10**9

xc = 4.8*10**12
yc = 2.4*10**12

planetsOld = [[1.9885*10**30, xc, yc, 0, 0, [0, 165, 255],13],
[0.33 * 10 ** 24, xc+5.79*10**10, yc, 0, 47900, [255, 255, 255],1], #mercury
[4.87 * 10 ** 24, xc+1.082*10**11, yc, 0, 35000, [255, 255, 255],1], #venus
[5.97 * 10 ** 24, xc+1.496*10**11, yc, 0, 29722, [165, 165, 0],3], #earth
[0.642 * 10 ** 24, xc+2.279*10**11, yc, 0, 24100, [0, 0, 255],2], #mars
[1898 * 10 ** 24, xc+7.786*10**11, yc, 0, 13100, [0, 200, 255],7], #jupiter
[568 * 10 ** 24, xc+1.4335*10**12, yc, 0, 9700, [0, 255, 255],5], #saturn
[86.8 * 10 ** 24, xc+2.8725*10**12, yc, 0, 6800, [255, 100, 100],4], #uranus
[102 * 10 ** 24, xc+4.4951*10**12, yc, 0, 5400, [255, 0, 0],5]] #Neptune
# [5 * 10 ** 6, xc+1.496*10**11+6.4*10**6, yc, 7100, 0, [255, 255, 255], 3]] #spaceship?

planetsNew = planetsOld

def update():
    global planetsOld, planetsNew,G,dt,h,w
    for p in range(len(planetsOld)):
        ax = 0
        ay = 0
        for i in planetsOld[:p]:
            a = i[1]-planetsOld[p][1]
            b = i[2]-planetsOld[p][2]
            const = G*planetsOld[p][0]*i[0]
            Fx = a*const/(a**2+b**2)**1.5
            Fy = b * const / (a ** 2 + b ** 2) ** 1.5
            ax = ax + Fx/planetsOld[p][0]
            ay = ay + Fy/planetsOld[p][0]
            # print(p,i,ax,ay,a,b)

        for i in planetsOld[p+1:]:
            a = i[1] - planetsOld[p][1]
            b = i[2] - planetsOld[p][2]
            const = G * planetsOld[p][0] * i[0]
            Fx = a * const / (a ** 2 + b ** 2) ** 1.5
            Fy = b * const / (a ** 2 + b ** 2) ** 1.5
            ax = ax + Fx / planetsOld[p][0]
            ay = ay + Fy / planetsOld[p][0]

        dvx = ax * dt
        dvy = ay * dt
        planetsNew[p][3] = planetsOld[p][3] + dvx
        planetsNew[p][4] = planetsOld[p][4] + dvy
        dx = planetsNew[p][3] * dt
        dy = planetsNew[p][4] * dt

        colorFrame([0,0,0],planetsOld[p][1],planetsOld[p][2],planetsNew[p][6])

        planetsNew[p][1] = planetsOld[p][1] + dx
        planetsNew[p][2] = planetsOld[p][2] + dy

        colorFrame(planetsOld[p][5],planetsNew[p][1],planetsNew[p][2], planetsNew[p][6])

    planetsOld = planetsNew

def colorFrame(color,x,y,size):
    global frame,h,w,scalar,h
    xscaled = int(x//(scalar))
    yscaled = int(y//(scalar))

    print(size, xscaled,yscaled)
    if yscaled < h and xscaled > 0:
        try:
            for i in range(size):
                for j in range(size):
                    frame[h-yscaled+size//2-i][xscaled+size//2-j] = color
        except:
            pass


while True:

    update()
    # print(planetsOld[0][3], planetsOld[1][3], planetsOld[1][1])

    cv2.imshow('output', frame)

    if cv2.waitKey(10) == ord('q'):
        # press q to terminate the loop
        cv2.destroyAllWindows()
        break
