import cv2
import numpy as np
capture = cv2.VideoCapture(0)  #'0'代表从摄像头读入，'./video.avi'代表读入视频
capture.isOpened()
num = 0
while 1:
    ret, frame = capture.read()
    cv2.imshow('testcamera', frame)
    key = cv2.waitKey(1)
    num += 1
    if key == 1048603:  # <ESC>
        break

capture.release()
cv2.destroyAllWindows()