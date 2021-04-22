# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

planets = cv.imread("cam.jpg")
planets1 = planets.copy()
for i in range(256):
    for j in range(256):
        if planets[i][j][0] < 100 and planets[i][j][1] < 100 and planets[i][j][2] > 200:
            planets[i][j] = [255, 255, 255]
        else:
            planets[i][j] = [0, 0, 0]

gay_img = cv.cvtColor(planets, cv.COLOR_BGRA2GRAY)
img = cv.medianBlur(gay_img, 13)  # 进行中值模糊，去噪点
circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 10, param1=100, param2=10, minRadius=4, maxRadius=20)
circles = np.uint16(np.around(circles))[0]
a = circles[0]

for i in range(256):
    for j in range(256):
        if planets1[i][j][0] < 100 and planets1[i][j][1] > 200 and planets1[i][j][2] < 100:
            planets1[i][j] = [255, 255, 255]
        else:
            planets1[i][j] = [0, 0, 0]

gay_img1 = cv.cvtColor(planets1, cv.COLOR_BGRA2GRAY)
img1 = cv.medianBlur(gay_img1, 13)  # 进行中值模糊，去噪点
circles1 = cv.HoughCircles(img1, cv.HOUGH_GRADIENT, 1, 10, param1=100, param2=10, minRadius=4, maxRadius=20)
circles1 = np.uint16(np.around(circles1))[0]
b = circles1[0]


img0 = plt.imread("cam.jpg")
print(a[0], a[1])
print(b[0], b[1])

fig = plt.figure('show picture')
ax = fig.add_subplot(111)
plt.imshow(img0)
plt.show()

# for i in range(l):
#     circle = Circle(xy=(x[i], y[i]), radius=r[i], alpha=1, color='b')
#     ax.add_patch(circle)
