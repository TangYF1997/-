#encoding=utf-8
import cv2
import numpy
face_patterns = cv2.CascadeClassifier('C:/Users/Administrator/PycharmProjects/face/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')  #加载分类器，在opencv库内
camera = cv2.VideoCapture(0) #这里是利用摄像头采集，打开摄像头操作
while camera.isOpened:
    #利用read方法读取摄像头的某一帧图片
    (ok, sample_image) = camera.read()
    if not ok:
        break

    faces = face_patterns.detectMultiScale(sample_image,scaleFactor=1.2,minNeighbors=3,minSize=(24, 24))
    for (x, y, w, h) in faces:
        cv2.rectangle(sample_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('face', sample_image)
    if cv2.waitKey(10)&0xFF==ord('q'):#按下q，退出循环
        break
camera.release()
#cv2.waitKey(0)
cv2.destroyAllWindows()