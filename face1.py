from aip import AipFace
import cv2
import urllib.request
import matplotlib.pyplot as plt
import math
import json
import ast
import numpy as np
from PIL import Image
from io import BytesIO
import base64


null = None  # 因为此处处理的是字符，所以此处定义为空字符串


def draw_point(face_field, image):
    # 根据图片中的特征点位置，在途中画出来，并标出特征点序号
    dict = face_field
    img = image
    pointNum = 0
    for value in dict.values():
        point = list(tuple(value.values()))
        a = 0
        for i in point:
            point[a] = int(i)
            a = a+1
        print(point)
        point = tuple(point)
        cv2.circle(img, point, 1, (0, 255, 0))
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.4
        thickness = 1
        cv2.putText(img, str(pointNum), point, font_face, font_scale, (0, 0, 0), thickness)
        pointNum = pointNum + 1


def frameFace(img, A, B, C, D):
    cv2.line(img, tuple(A), tuple(B), (0, 0, 255), 1)
    cv2.line(img, tuple(B), tuple(C), (0, 0, 255), 1)
    cv2.line(img, tuple(C), tuple(D), (0, 0, 255), 1)
    cv2.line(img, tuple(D), tuple(A), (0, 0, 255), 1)


def getFaceLocation(location):
    # 根据输入的图片和位置信息，将图片框出来，返回4个端点的坐标
    Theta = location['rotation'] / 60  # 注意：为啥是60度，自己多次测试的结果，必须得弄清楚rotation啥意思，相对于哪里的旋转角度
    A = [int(location['left']), int(location['top'])]
    B = [int(location['left']) + int(location['width'] * math.cos(Theta)),
         int(location['top']) + int(location['width'] * math.sin(Theta))]
    AC_Len = math.sqrt(location['width'] ** 2 + location['height'] ** 2)
    AC_Theta = math.atan(location['height'] / location['width']) + location['rotation'] / 60
    C = [int(location['left']) + int(AC_Len * math.cos(AC_Theta)),
         int(location['top']) + int(AC_Len * math.sin(AC_Theta))]
    D = [int(location['left']) - int(location['height'] * math.sin(Theta)),
         int(location['top']) + int(location['height'] * math.cos(Theta))]
    return A, B, C, D


def frame2base64(frame):
    # 将视屏中的一帧图片转换成base64格式 返回base64编码
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data_img = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data_img


def rotate(img, num, A, B, C, D, rotation):
    # 输入4个端点的坐标和旋转角度，将图片旋转后输出，并保存在文件夹中
    # withRect = math.sqrt((D[0] - A[0]) ** 2 + (D[1] - A[1]) ** 2) # 矩形宽度
    # heightRect = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)# 矩形高度
    angle = rotation  # 矩形框旋转角度
    height = img.shape[0]  # 原始图像高度
    width = img.shape[1]  # 原始图像宽度
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
    heightNew = int(width * math.fabs(math.sin(math.radians(angle))) + height * math.fabs(math.cos(math.radians(angle))))
    widthNew = int(height * math.fabs(math.sin(math.radians(angle))) + width * math.fabs(math.cos(math.radians(angle))))
    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))
    A1 = A[:]
    B1 = B[:]
    C1 = C[:]
    D1 = D[:]
    # 旋转后图像的四点坐标
    [[A[0]], [A[1]]] = np.dot(rotateMat, np.array([[A[0]], [A[1]], [1]]))
    [[C[0]], [C[1]]] = np.dot(rotateMat, np.array([[C[0]], [C[1]], [1]]))
    [[B[0]], [B[1]]] = np.dot(rotateMat, np.array([[B[0]], [B[1]], [1]]))
    [[D[0]], [D[1]]] = np.dot(rotateMat, np.array([[D[0]], [D[1]], [1]]))
    outWidth = int(D[1])-int(B[1])
    outLong = int(A[0])-int(C[0])

    imgOut = imgRotation[int(B[1])-int(outWidth/4):int(D[1]+int(outWidth/4)), int(A[0])+int(outLong/4):int(C[0])-int(outLong/4)]
    cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\' + str(num) + '.png', imgOut)
    return imgOut, A1, B1, C1, D1


def recognition(img1, filepath, threshold):
    # 将两张图片进行对比，输入两张图片和阈值，判断是不是同一个人
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    # output_buffer = BytesIO()  # 创建一个BytesIO
    # img1.save(output_buffer, format='JPEG')  # 写入output_buffer
    # byte_data = output_buffer.getvalue()  # 在内存中读取
    # img1_base64_data = base64.b64encode(byte_data)  # 转为BASE64
    # img2.save(output_buffer, format='JPEG')  # 写入output_buffer
    # byte_data = output_buffer.getvalue()  # 在内存中读取
    # img2_base64_data = base64.b64encode(byte_data)  # 转为BASE64

    img1_base64_data = frame2base64(img1)   # 将图片转成base64格式

    with open(filepath, "rb") as fp:
        img2_base64_data = base64.b64encode(fp.read())

    params = json.dumps(
        [{"image": '' + str(img1_base64_data, 'utf-8') + '', "image_type": "BASE64", "face_type": "LIVE",
          "quality_control": "LOW"},
         {"image": '' + str(img2_base64_data, 'utf-8') + '', "image_type": "BASE64", "face_type": "IDCARD",
          "quality_control": "LOW"}])
    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        print(content)
    content = content.decode("utf-8")
    if content[14] != '0':
        str1 = content[34:60]
        # print(str1.index('"'))
        print(str1)
        return str1
    else:
        content = ast.literal_eval(content)
        print(content['result']['score'])
        if content['result']['score'] >= threshold:
            # tkinter.messagebox.showinfo('图片相似度', "两个人的相似度为：%d" % content['result']['score'] + "%"+"     是同一人")
            print("两个人的相似度为：%d" % content['result']['score'] + "%"+"\r"+"     是同一人")
            return 1
        else:
            # tkinter.messagebox.showinfo('图片相似度', "两个人的相似度为：%d" % content['result']['score'] + "%"+"     不是同一人")
            print("两个人的相似度为：%d" % content['result']['score'] + "%"+"\r"+"     不是同一人")
            return 0


def search(img):
    # 输入人脸图片，在百度人脸库中对应出学生信息，返回id或姓名
    request_search_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    img1_base64 = frame2base64(img)  # 将图片转成base64格式

    img_base64_utf_8 = str(img1_base64, 'utf-8')

    params = "{\"image\":\"" + img_base64_utf_8 + "\",\"image_type\":\"BASE64\",\"group_id_list\":\"DX1501\",\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\"}"
    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_search_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        print(content)
    content = content.decode("utf-8")
    if content[14] != '0':
        str1 = content[33:60]
        print(str1)
    else:
        content = ast.literal_eval(content)
        print('学生id为' + str(content['result']['user_list'][0]['user_id']))
        print('相似度为' + str(content['result']['user_list'][0]['score']))
        return str(content['result']['user_list'][0]['user_id'])

# 定义常量


APP_ID = '15647216'
API_KEY = 'lDsbbF6YmdtpdwdjZyIz08aF'
SECRET_KEY = '2MBLkXYOVmGUjqPEfxKD8Wwz3lwzLSoW'

# 初始化AipFace对象
aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)


# filename = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\2.jpg'
# img2 = open(filename, 'rb')


camera = cv2.VideoCapture(0) # 这里是利用摄像头采集，打开摄像头操作
while camera.isOpened:
    # 利用read方法读取摄像头的某一帧图片
    (ok, sample_image) = camera.read()
    # cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\2.png', sample_image)
    # filepath = "C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\2.png"
    # with open(filepath, "rb") as fp:
    #     a = fp.read()
    #     base64_data = base64.b64encode(a)
    #
    # image = cv2.imencode('.png', sample_image)
    # base64_data = base64.b64encode(image)

    base64_data = frame2base64(sample_image)

    image64 = str(base64_data, 'utf-8')
    imageType = "BASE64"

    if not ok:
        break

    options = {}
    options["face_field"] = "landmark150"
    options["max_face_num"] = 10
    options["face_type"] = "LIVE"

    # 调用人脸属性检测接口
    # t1 = cv2.getTickCount()
    result = aipFace.detect(image64, imageType, options)

    if result['result'] == None:
        cv2.imshow('img', sample_image)
        cv2.waitKey(1000)
        continue
    # 解析位置信息
    face_num = result['result']['face_num']
    # t2 = (cv2.getTickCount() - t1) / cv2.getTickFrequency()
    t1 = cv2.getTickCount()
    for num in range(0, int(face_num)):
        location = result['result']['face_list'][num - 1]['location']
        face_field = result['result']['face_list'][num - 1]['landmark150']
        # draw_point(face_field,sample_image)       # 画出特征点
        # print(location)
        # print(location['face_list'][0])

        (A,B,C,D) = getFaceLocation(location)      # 返回4个端点的坐标

        (imgRotation,A1,B1,C1,D1) = rotate(sample_image, num, A, B, C, D, location['rotation'])  # 将图片中框出来的人脸旋转后输出

        frameFace(sample_image,A1,B1,C1,D1)

        plt.imshow(imgRotation)

        plt.show()

        # rato = recognition(imgRotation,filename,80)          # 识别
        id = search(imgRotation)                             # 在百度人脸库中搜索该人脸，返回人脸的id
        cv2.putText(sample_image, str(id), tuple(A1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    t2 = (cv2.getTickCount() - t1)/cv2.getTickFrequency()
    print(t2)
    cv2.imshow('img', sample_image)

    # left_top = (int(location['left']),int(location['top']))
    # right_bottom = (left_top[0]+int(location['width']),left_top[1]+int(location['height']))
    # cv2.rectangle(img,left_top, right_bottom, (0,0,255),2)

    #    faces = face_patterns.detectMultiScale(sample_image,scaleFactor=1.1,minNeighbors=5,minSize=(80, 80))
#    for (x, y, w, h) in faces:
#        cv2.rectangle(sample_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#    cv2.imshow('face', sample_image);
    if cv2.waitKey(1000)&0xFF==ord('q'):  # 按下q，退出循环
        break
camera.release()
#
