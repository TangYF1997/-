# coding=utf-8
import time
time1 = time.time()
import cv2
image = cv2.imread("C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\js_2_big.jpg")
res = cv2.resize(image, (4000, 3000), interpolation=cv2.INTER_AREA)
cv2.imwrite("C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\js_2_compressed.jpg", res)
time2=time.time()
print ('总共耗时：' + str(time2 - time1) + 's')
