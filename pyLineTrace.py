#coding: utf-8
import numpy as np
import cv2
import time


def LSMETHOD(x, y):
    print(np.polyfit(y, x, 1))

#==== variable ====#
LOOPCNT = 10000
LOOPTIME = 3
MAXHEIGHT = 200
RANGE = MAXHEIGHT / LOOPTIME
maskLower = np.array([0, 0, 0])
maskUpper = np.array([180, 255, 170])
aveTime = 0

cap = cv2.VideoCapture(0)
Img = cv2.imread('raspicamera.jpg')
ret, Img = cap.read()
height, width, ch = Img.shape

for a in range(LOOPCNT):
    ret, Img = cap.read()
    cpImg = Img.copy()

    start = time.time()

    for y in range(LOOPTIME):
        middle_point_xcoordinate = np.zeros(6, dtype = np.int16)
        middle_point_ycoordinate = np.zeros(6, dtype = np.uint16)
        aveXCoordinate = 0
        count = 0
        upper = height - RANGE*y -3

        hsvImg = cv2.cvtColor(cpImg[upper:upper +3, 0:width], cv2.COLOR_BGR2HSV)
        maskRoi = cv2.inRange(hsvImg, maskLower, maskUpper)
        filteredImg = cv2.medianBlur(maskRoi, ksize=3)
        for i in range(width):
            if(filteredImg[1, i] == 255):
                aveXCoordinate += i
                count += 1
        aveXCoordinate /= (count+1)
        aveXCoordinate -= width / 2
        middle_point_xcoordinate[y] = aveXCoordinate
        middle_point_ycoordinate[y] = RANGE * y
        cv2.circle(cpImg, (aveXCoordinate + (width / 2), height - RANGE*y), 10, (142, 255, 142), -1)

    cv2.imshow('result',cpImg)

    if cv2.waitKey(1) & 0xff == ord('q'):
        cv2.destroyAllWindows()
        break

    LSMETHOD(middle_point_xcoordinate, middle_point_ycoordinate)
    end = time.time()
    aveTime += (start - end)

    print("time = " + str(aveTime/LOOPCNT) + "[sec]")
