import cv2
import matplotlib.pyplot as plt

face_patterns = cv2.CascadeClassifier('C:/Users/Administrator/PycharmProjects/face/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')

sample_image = cv2.imread('C:\\Users\\Administrator\\PycharmProjects\\untitled\\12.jpg')

gray = cv2.cvtColor(sample_image, cv2.COLOR_BGR2GRAY)

equ = cv2.equalizeHist(gray)

faces = face_patterns.detectMultiScale(sample_image,scaleFactor=1.1,minNeighbors=5,minSize=(20, 20))

num = 0

for (x, y, w, h) in faces:
    cv2.rectangle(sample_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    face1 = sample_image[y:y+w, x:x+h]
    plt.imshow(face1, 'gray')
    plt.show()
    cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\'+str(num)+'.png', face1)
    num = num + 1

cv2.imshow('img', sample_image)

cv2.waitKey(0)
