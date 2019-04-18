from aip import AipFace
import cv2
import urllib.request as urllib2
import matplotlib.pyplot as plt
import math
import ast
import numpy as np
from PIL import Image
from io import BytesIO
import base64
'''
人脸搜索
'''


def getFaceLocation(location):
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
# 根据输入的图片和位置信息，将图片框出来，返回4个端点的坐标


def frameFace(img, A, B, C, D):
    cv2.line(img, tuple(A), tuple(B), (0, 0, 255), 1)
    cv2.line(img, tuple(B), tuple(C), (0, 0, 255), 1)
    cv2.line(img, tuple(C), tuple(D), (0, 0, 255), 1)
    cv2.line(img, tuple(D), tuple(A), (0, 0, 255), 1)
# 在图上根据坐标画框


def rotate(img, num, A, B, C, D, rotation):
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
    [[A1[0]], [A1[1]]] = np.dot(rotateMat, np.array([[A1[0]], [A1[1]], [1]]))
    [[C1[0]], [C1[1]]] = np.dot(rotateMat, np.array([[C1[0]], [C1[1]], [1]]))
    [[B1[0]], [B1[1]]] = np.dot(rotateMat, np.array([[B1[0]], [B1[1]], [1]]))
    [[D1[0]], [D1[1]]] = np.dot(rotateMat, np.array([[D1[0]], [D1[1]], [1]]))
    outWidth = int(D1[1])-int(B1[1])
    outLong = int(A1[0])-int(C1[0])

    imgOut = imgRotation[int(B1[1])-int(outWidth/4):int(D1[1]+int(outWidth/4)), int(A1[0])+int(outLong/4):int(C1[0])-int(outLong/4)]
    # cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\' + str(num) + '.png', imgOut)
    return imgOut
# 输入4个端点的坐标和旋转角度，将图片旋转


def search_face(filepath, group_id_list):
    request_multi_search_url = "https://aip.baidubce.com/rest/2.0/face/v3/multi-search"
    # filepath = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\3.png'

    sample_image = cv2.imread(filepath)
    with open(filepath, "rb") as fp:
        base64_data = base64.b64encode(fp.read())
    img_base64_utf_8 = str(base64_data, 'utf-8')
    # print(img_base64_utf_8)

    t1 = cv2.getTickCount()

    params = "{\"image\":\"" + img_base64_utf_8 + " \",\"image_type\":\"BASE64\",\"group_id_list\":\""+group_id_list+"\",\"max_face_num\" : 10,\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_multi_search_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    t2 = (cv2.getTickCount() - t1) / cv2.getTickFrequency()
    print(t2)
    if content:
        print(content)
    content = content.decode("utf-8")
    if content[14] != '0':
        str1 = content[33:50]
        print(str1)
    else:
        content = ast.literal_eval(content)
        for num in range(0, int(content['result']['face_num'])):
            if content['result']['face_list'][num - 1]['user_list'] == []:
                print('该学生不再库中')
            else:
                if content['result']['face_list'][num - 1]['user_list'][0]['user_id'] == 9:
                    print("9来了")
                print('学生id为' + str(content['result']['face_list'][num - 1]['user_list'][0]['user_id']))
                print('相似度为' + str(content['result']['face_list'][num - 1]['user_list'][0]['score']))
            location = content['result']['face_list'][num - 1]['location']
            (A, B, C, D) = getFaceLocation(location)
            imgRotation = rotate(sample_image, num, A, B, C, D,
                                                   location['rotation'])  # 将图片中框出来的人脸旋转后输出
            frameFace(sample_image, A, B, C, D)
        plt.imshow(sample_image)
        plt.show()
        cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\23.jpg', sample_image)


'''
输入图片路径和已知的人脸组，将图中所有的人脸和人脸库中的人脸进行对比，得出图片中人的考勤信息
将学生的考勤信息输出
'''


# for i in range(1,34):
#     filepath = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\'+str(i)+'.png'
#     search_face(filepath, group_id_list="DX1502")


