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

G = 6.647*10**-11
dt = 1
# scalar = 2.496*10**8
scalar = 0.75*10**6

xc = 750*scalar
yc = 400*scalar

earthR = 6.378*10**6
FT = 74.5*10**6
dm = 716*dt
dragCoeff = 0.82
rocketA = 63.61

planetsOld = [[4.9*10**6, xc+earthR,yc, 0, 460, [255, 255, 255],30],
[5.97 * 10 ** 24, xc, yc, 0, -12.5097, [165, 165, 0],1.2756*10**7], #earth
[0.073 * 10 ** 24, xc+3.84467*10**8, yc, 0, 1023.055, [255, 255, 255], 3.476*10**6]]  #moon

planetsNew = planetsOld

def update():
    global planetsOld, planetsNew,G,dt,h,w, earthR,FT,dm,dragCoeff,rocketA
    for p in range(len(planetsOld)):
        Fx = 0
        Fy = 0
        for i in planetsOld[:p]:
            a = i[1]-planetsOld[p][1]
            b = i[2]-planetsOld[p][2]
            const = G*planetsOld[p][0]*i[0]
            Fx = Fx + a*const/(a**2+b**2)**1.5
            # print(p,Fx,a,b)
            Fy = Fy + b * const / (a ** 2 + b ** 2) ** 1.5

        for i in planetsOld[p+1:]:
            a = i[1] - planetsOld[p][1]
            b = i[2] - planetsOld[p][2]
            const = G * planetsOld[p][0] * i[0]
            Fx = Fx + a * const / (a ** 2 + b ** 2) ** 1.5
            Fy = Fy + b * const / (a ** 2 + b ** 2) ** 1.5

        if p == 0:
            a = planetsOld[p][1] - planetsOld[1][1]
            b = planetsOld[p][2] - planetsOld[1][2]
            hyp = math.sqrt(a**2 + b**2)
            if planetsOld[p][0] <= 1.5*10**6:
                FT = 0
                dm = 0
            FTx = FT*a/hyp
            FTy = FT*b/hyp

            V_2 = (planetsOld[p][3]**2 + planetsOld[p][4]**2)
            delta = hyp - earthR
            rho = getDensity(delta)
            Fd = 0.5*rho*dragCoeff*rocketA*V_2
            Fdx = Fd*a/hyp
            Fdy = Fd*b/hyp

            print(Fx,FTx,Fdx,planetsOld[p][3],rho,delta)

            Fx = Fx + FTx - Fdx
            Fy = Fy + FTy - Fdy


            planetsNew[p][0] = planetsOld[p][0] - dm


        ax = Fx / planetsOld[p][0]
        ay = Fy / planetsOld[p][0]
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
    # print(planetsOld[0][0])

def getDensity(delta):
    dens = 0

    if delta <= 20000:
        print(1)
        Hn = 10400
        dens = 1.2*math.e**(-delta/Hn)
    elif delta > 20000 and delta < 1*10**5:
        print(2)
        Hn = 6300
        rhoU = 1.2*math.e**(-20000/10400)
        dens = rhoU*math.e**(-(delta-20000)/Hn)
    else:
        print(3)
        dens = 0
    return dens

def colorFrame(color,x,y,size):
    global frame,h,w,scalar,h
    xscaled = int(x//(scalar))
    yscaled = int(y//(scalar))

    sizeScaled = int(size//scalar)
    if sizeScaled == 0:
        sizeScaled = 1

    if sizeScaled%2 == 1:
        r = sizeScaled//2 + 1
    else:
        r = sizeScaled//2

    # if size == 30:
    #     print(xscaled,yscaled)

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
    seconds = t
    minutes = (t//60)
    hours = (t//3600)
    days = (hours//24)
    months = (days//30)
    years = int(days//365)
    seconds = int(seconds%60)
    minutes = int(minutes%60)
    hours = int(hours%24)
    days = int(days%30)
    months = int(months%12)
    # print(years,months,days,hours,minutes,seconds)
    displayNumber(str(years)+','+str(months)+','+str(days)+','+str(hours)+','+str(minutes)+','+str(seconds))

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
