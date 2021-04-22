# -*- coding: utf-8 -*-
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from controller import Supervisor

# time in [ms] of a simulation step
TIME_STEP = 1600
img_name = "./cam_" + str(os.getpid()) + ".jpg"

# create the Robot instance.
robot = Supervisor()

print(img_name)
robot.step(1000)
camera = robot.getDevice('camera')
camera.enable(64)
camera.saveImage(img_name, 100)

while robot.step(TIME_STEP) != -1:
    camera.saveImage(img_name, 100)
    planets = cv.imread(img_name)
    planets_copy = planets.copy()
    for i in range(256):
        for j in range(256):
            if planets[i][j][0] < 100 and planets[i][j][1] < 100 and planets[i][j][2] > 200:
                planets[i][j] = [255, 255, 255]
            elif planets[i][j][0] < 100 and planets[i][j][1] > 200 and planets[i][j][2] < 100:
                planets[i][j] = [255, 255, 255]
            else:
                planets[i][j] = [0, 0, 0]

    img0 = plt.imread(img_name)
    fig = plt.figure('show picture')
    ax = fig.add_subplot(111)

    gay_img = cv.cvtColor(planets, cv.COLOR_BGRA2GRAY)
    img = cv.medianBlur(gay_img, 13)  # 进行中值模糊，去噪点
    circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 15, param1=100, param2=10, minRadius=5, maxRadius=20)

    circles = np.uint16(np.around(circles))
    circles = circles[0]
    a = circles[0]
    b = circles[1]

    if img0[a[1]][a[0]][0] > 200 and img0[a[1]][a[0]][1] < 100 and img0[a[1]][a[0]][2] < 100:
        print(a[0], a[1], "/", '%.3f' % robot.getFromDef("robot-1").getPosition()[0],
              '%.3f' % robot.getFromDef("robot-1").getPosition()[2])
        print(b[0], b[1], "/", '%.3f' % robot.getFromDef("robot-2").getPosition()[0],
              '%.3f' % robot.getFromDef("robot-2").getPosition()[2])
    else:
        print(b[0], b[1], "/", '%.3f' % robot.getFromDef("robot-1").getPosition()[0],
              '%.3f' % robot.getFromDef("robot-1").getPosition()[2])
        print(a[0], a[1], "/", '%.3f' % robot.getFromDef("robot-2").getPosition()[0],
              '%.3f' % robot.getFromDef("robot-2").getPosition()[2])
    print("-----------------------")
