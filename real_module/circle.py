# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

planets = cv.imread("cam.jpg")
for i in range(256):
    for j in range(256):
        if planets[i][j][0] < 100 and planets[i][j][1] < 100 and planets[i][j][2] > 200:
            planets[i][j] = [255, 255, 255]
        elif planets[i][j][0] < 100 and planets[i][j][1] > 200 and planets[i][j][2] < 100:
            planets[i][j] = [255, 255, 255]
        else:
            planets[i][j] = [0, 0, 0]

img0 = plt.imread("cam.jpg")
fig = plt.figure('show picture')
ax = fig.add_subplot(111)

gay_img = cv.cvtColor(planets, cv.COLOR_BGRA2GRAY)
img = cv.medianBlur(gay_img, 13)  # 进行中值模糊，去噪点
circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 10, param1=100, param2=10, minRadius=4, maxRadius=20)

circles = np.uint16(np.around(circles))
circles = circles[0]
a = circles[0]
b = circles[1]

if img0[a[1]][a[0]][0] > 200 and img0[a[1]][a[0]][1] < 100 and img0[a[1]][a[0]][2] < 100:
    print(a[0], a[1])
    print(b[0], b[1])
else:
    print(b[0], b[1])
    print(a[0], a[1])

plt.imshow(img0)
plt.show()

# l = len(circles)
# x = [0] * l
# y = [0] * l
# r = [0] * l
# for i in range(l):
#     x[i] = circles[i][0]
#     y[i] = circles[i][1]
#     r[i] = circles[i][2]
#
# for i in range(l):
#     circle = Circle(xy=(x[i], y[i]), radius=r[i], alpha=1, color='b')
#     ax.add_patch(circle)
# plt.plot(x, y, 'b.')
# # ax.imshow(img0)
# ax.imshow(img0)
# # plt.axis('off')  # 不显示刻度
# plt.show()
