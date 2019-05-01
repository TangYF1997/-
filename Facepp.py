import requests
import ast
import cv2
import matplotlib.pyplot as plt
import urllib.request as urllib2
import urllib
import math
from io import BytesIO
import base64
from PIL import Image
import numpy as np

'''
调用Face++的API来实现将一张高清原图中的人脸聚集部分切割下来，然后分块，方便百度人脸M:N搜索
'''
null = ''


'''
图像对比度增强
'''


def contrast_enhance(img_base64):
    request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/contrast_enhance"

    params = {"image": img_base64}
    params = urllib.parse.urlencode(params)

    access_token = '24.52e67e0599cb4127b965e29c0409b964.2592000.1559116211.282335-16141688'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    try:
        img = content['image']
    except Exception:
        print("图像出错了")
    finally:
        return img


def get_face_location(location):
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


def search_face(image_box, student_list, image, box, group_id_list):
    request_multi_search_url = "https://aip.baidubce.com/rest/2.0/face/v3/multi-search"
    # filepath = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\3.png'

    # sample_image = cv2.imread(filepath)
    # with open(filepath, "rb") as fp:
    #     base64_data = base64.b64encode(fp.read())
    # img_base64_utf_8 = str(base64_data, 'utf-8')
    # print(img_base64_utf_8)
    #
    # global null
    img_base64 = PIL2base64(image_box)

    # img_base64_utf_8 = contrast_enhance(img_base64)

    img_base64_utf_8 = str(img_base64, 'utf-8')

    params = "{\"image\":\"" + img_base64_utf_8 + " \",\"image_type\":\"BASE64\",\"group_id_list\":\""+group_id_list+"\",\"max_face_num\" : 10,\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_multi_search_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()

    # if content:
    #     print(content)
    content = content.decode("utf-8")
    content = eval(content)
    print(content)
    if content['error_code'] != 0:
        str1 = content['error_msg']
        print(str1)
    else:
        # content = ast.literal_eval(content)
        for num in range(0, int(content['result']['face_num'])):
            if content['result']['face_list'][num - 1]['user_list'] == []:
                user_id = "Unknown"
                print('该学生不再库中')
            else:
                user_id = str(content['result']['face_list'][num - 1]['user_list'][0]['user_id'])
                print('学生id为' + str(content['result']['face_list'][num - 1]['user_list'][0]['user_id']))
                student_list.append(user_id)
                print('相似度为' + str(content['result']['face_list'][num - 1]['user_list'][0]['score']))
            location = content['result']['face_list'][num - 1]['location']
            (A, B, C, D) = get_face_location(location)
            A = [A[0] + box[0], A[1] + box[1]]
            B = [B[0] + box[0], B[1] + box[1]]
            C = [C[0] + box[0], C[1] + box[1]]
            D = [D[0] + box[0], D[1] + box[1]]
            frameFace(image, A, B, C, D, user_id)
            # imgRotation = rotate(sample_image, num, A, B, C, D,
            #                                        location['rotation'])  # 将图片中框出来的人脸旋转后输出
            # frameFace(sample_image, A, B, C, D)
        # plt.imshow(sample_image)
        # plt.show()
        # cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\23.jpg', sample_image)
    return student_list
# 返回ABCD四点坐标，是在输入图像中的坐标，后面要在原图显示得处理一下


def resize_img(image_cv2):
    width = image_cv2.shape[1]  # 8000
    height = image_cv2.shape[0]  # 6000
    resized_img = cv2.resize(image_cv2, (int(width/2), int(height/2)), interpolation=cv2.INTER_AREA)
    return resized_img


def resize_pil_image(img_pil):
    size = img_pil.size
    im_resized = img_pil.resize(int(size[0]/2), int(size[1]/2))
    return im_resized


def show_images(image_list):
    index = 1
    for image in image_list:
        image.save('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\' + str(index) + '.png')
        plt.imshow(image)
        plt.show()
        index += 1


# def rotate(img, num, A, B, C, D, rotation):
#     angle = rotation  # 矩形框旋转角度
#     height = img.shape[0]  # 原始图像高度
#     width = img.shape[1]  # 原始图像宽度
#     rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
#     heightNew = int(
#         width * math.fabs(math.sin(math.radians(angle))) + height * math.fabs(math.cos(math.radians(angle))))
#     widthNew = int(height * math.fabs(math.sin(math.radians(angle))) + width * math.fabs(math.cos(math.radians(angle))))
#     rotateMat[0, 2] += (widthNew - width) / 2
#     rotateMat[1, 2] += (heightNew - height) / 2
#     imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))
#
#     # 旋转后图像的四点坐标
#     [[A[0]], [A[1]]] = np.dot(rotateMat, np.array([[A[0]], [A[1]], [1]]))
#     [[C[0]], [C[1]]] = np.dot(rotateMat, np.array([[C[0]], [C[1]], [1]]))
#     [[B[0]], [B[1]]] = np.dot(rotateMat, np.array([[B[0]], [B[1]], [1]]))
#     [[D[0]], [D[1]]] = np.dot(rotateMat, np.array([[D[0]], [D[1]], [1]]))
#
#     img_out = imgRotation[int(B[1]):int(D[1]), int(A[0]):int(C[0])]
#     cv2.imwrite('C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\' + str(num) + '.png', img_out)
#     return imgRotation  # rotated image


def frameFace(img, A, B, C, D, user_id):
    cv2.line(img, tuple(A), tuple(B), (0, 0, 255), 2)
    cv2.line(img, tuple(B), tuple(C), (0, 0, 255), 2)
    cv2.line(img, tuple(C), tuple(D), (0, 0, 255), 2)
    cv2.line(img, tuple(D), tuple(A), (0, 0, 255), 2)
    cv2.putText(img, user_id, tuple(A), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# 在图上根据坐标画框


def box_search(image_PIL, image_cv2, box_list, group):
    student_list = []
    for box in box_list:
        image_box = image_PIL.crop(box)  # 此图为切割后的一个部分图像
        image_size = image_box.size
        if image_size[1] > 1000:
            image_box = resize_pil_image(image_box)
        student_list = search_face(image_box, student_list, image_cv2, box, group)  # 这里的group_list后面会变成变量
    return student_list


def frame2base64(frame):
    # 将视屏中的一帧图片转换成base64格式 返回base64编码
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data_img = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data_img


def PIL2base64(img):
    # 将视屏中的一帧图片转换成base64格式 返回base64编码
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data_img = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data_img


def cut_image(image, cv2_img, min_left_ratio, max_right_ratio, min_top_ratio, max_bottom_ratio, max_length_of_frame_ratio):
    image_width, img_height = image.size
    min_left = int(min_left_ratio * image_width)
    max_right = int(max_right_ratio * image_width)
    min_top = int(min_top_ratio * img_height)
    max_bottom = int(max_bottom_ratio * img_height)
    max_length_of_frame = int(max_length_of_frame_ratio * img_height)
    main_height = max_bottom - min_top  # 中间人脸集中部分的上下长度
    main_width = max_right - min_left  # 中间人脸集中部分的左右长度
    length_width_ratio = int(main_width / main_height) + 1  # 长宽比

    print(length_width_ratio)  # 输出主要图片的长宽比
    # box = (min_left, min_top, max_right, max_down - int(main_width/3))
    # box = (min_left, min_top, max_right, max_bottom)  # 切割出主要部分

    layer_height = []
    layer_top = []  # 存储三个层的顶部信息，后面要将其改为按原图的比例
    layer_bottom = []  # 存储三个层的底部信息，后面要将其改为按原图的比例

    # 第三层（最上层）的高度，1/4个图片的高度 从这里到1/4图像处
    layer_top.append(min_top)
    layer_bottom.append(min_top + int(main_height / 4))
    layer_height.append(layer_bottom[0] - layer_top[0])

    # 第二层（中间层）的高度，1/4个图片的高度+ 最大人脸的高度的一半，差不多1/3个图片高 从这里到1/2图像处
    layer_top.append(int(main_height / 4 - max_length_of_frame / 2) + min_top)
    layer_bottom.append(max_bottom - int(main_height / 2))
    layer_height.append(layer_bottom[1] - layer_top[1])

    # 最下层的高度，1/2个图片的高度+ 最大人脸的高度，差不多2/3个图片高 从这里到最大值处
    layer_top.append(int(main_height / 2 - max_length_of_frame) + min_top)
    layer_bottom.append(max_bottom)
    layer_height.append(layer_bottom[2] - layer_top[2])

    # image = image.crop(box)  # 此图为去除无关部分后的图像

    box_list = []
    count = 0
    for j in range(0, 3):
        item_width = layer_height[j]
        for i in range(0, int(main_width / item_width)):
            count += 1
            box = (i * item_width + min_left, layer_top[j],
                   (i + 1) * item_width + min_left + int(max_length_of_frame / (3 - j)),
                   layer_bottom[j])  # (左上横，纵，右下横，纵)
            cv2.line(cv2_img, (i * item_width + min_left, layer_top[j]),
                     (i * item_width + min_left, layer_bottom[j]), (0, 0, 255), 2)
            cv2.line(cv2_img, ((i + 1) * item_width + min_left + int(max_length_of_frame / (3 - j)), layer_top[j]),
                     ((i + 1) * item_width + min_left + int(max_length_of_frame / (3 - j)), layer_bottom[j]),
                     (0, 0, 255),
                     2)
            box_list.append(box)
    print(count)
    # image_list = [image.crop(box) for box in box_list]
    #
    # show_images(image_list)

    cv2.line(cv2_img, (min_left, min_top), (max_right, min_top), (0, 0, 255), 2)
    # print(min_top)
    cv2.line(cv2_img, (min_left, min_top + int(main_height)), (max_right, min_top + int(main_height)), (0, 0, 255), 2)
    cv2.line(cv2_img, (min_left, layer_top[2]), (max_right, layer_top[2]), (0, 0, 255), 2)
    cv2.line(cv2_img, (min_left, layer_top[1]), (max_right, layer_top[1]), (0, 0, 255), 2)
    # cv2.line(cv2_img, (0, min_top + layer1_height), (main_length, min_top + layer1_height), (0, 0, 255), 2)
    cv2.line(cv2_img, (min_left, min_top + int(main_height / 4)), (max_right, min_top + int(main_height / 4)),
             (0, 0, 255), 2)  # 图像1/4 处
    cv2.line(cv2_img, (min_left, min_top + int(main_height / 2)), (max_right, min_top + int(main_height / 2)),
             (0, 0, 255), 2)  # 图像1/2 处

    plt.imshow(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    plt.show()

    return box_list, count


'''
根据比例切割原图
'''


def frame_face(image_compressed, response_content):

    global min_left_ratio1, max_right_ratio1, min_top_ratio1, max_bottom_ratio1, max_length_of_frame_ratio1
    image_width, image_height = image_compressed.size
    face_num = len(response_content['faces'])

    value1 = []
    value2 = []
    value3 = []
    value4 = []
    length_of_frame = []

    for num in range(0, int(face_num)):
        location = response_content['faces'][num - 1]['face_rectangle']
        point_A = [int(location['left'])*2, int(location['top'])*2]
        point_B = [int(location['left'])*2 + int(location['width'])*2, int(location['top'])*2]
        point_C = [int(location['left'])*2 + int(location['width'])*2, int(location['top'])*2 + int(location['height'])*2]
        point_D = [int(location['left'])*2, int(location['top'])*2 + int(location['height'])*2]

        value1.append(point_A[0])  # 最左值
        value2.append(point_A[1])  # 最上值
        value3.append(point_C[0])  # 最右值
        value4.append(point_C[1])  # 最下值
        length_of_frame.append(int(location['width']))

        # cv2.line(cv2_img, tuple(point_A), tuple(point_B), (0, 0, 255), 2)
        # cv2.line(cv2_img, tuple(point_B), tuple(point_C), (0, 0, 255), 2)
        # cv2.line(cv2_img, tuple(point_C), tuple(point_D), (0, 0, 255), 2)
        # cv2.line(cv2_img, tuple(point_D), tuple(point_A), (0, 0, 255), 2)
        min_left = min(value1)  # 人脸集中处的最左端，后面要将其改为按原图的比例
        max_right = max(value3)  # 人脸集中处的最右端，后面要将其改为按原图的比例
        min_top = min(value2)  # 人脸集中处的最上端，后面要将其改为按原图的比例
        max_bottom = max(value4)  # 人脸集中处的最下端，后面要将其改为按原图的比例
        max_length_of_frame = max(length_of_frame)  # 最大的人脸框大小，后面要将其改为按原图的比例

        min_left_ratio1 = min_left / (image_width*2)
        max_right_ratio1 = max_right / (image_width*2)
        min_top_ratio1 = min_top / (image_height*2)
        max_bottom_ratio1 = max_bottom / (image_height*2)
        max_length_of_frame_ratio1 = max_length_of_frame / image_height
        # 这里不除二 是因为图片占全图的比例是占API用的图片的，其他的都是占的原图

    return min_left_ratio1, max_right_ratio1, min_top_ratio1, max_bottom_ratio1, max_length_of_frame_ratio1


'''
    这个函数用来实现将压缩后的图片使用Face++API处理后，根据的其返回的内容处理得到
    1.主要人脸图的上下左右位置信息占原图片的比例
    2.图中最大人脸框的大小占图高的比例
    '''

def attendance_system(filepath, group):
    t1 = cv2.getTickCount()
    http_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"  # 你要调用API的URL
    key = "qFlVJKRVTBaku9Z7RN88Il6uYqcUXVjP"
    secret = "_R-LS6ogjkqiJtSBFDHDicrm025_5Ohq"  # face++提供的一对密钥

    cv2_img = cv2.imread(filepath)  # cv2 的图像
    cv2_img_resized = resize_img(cv2_img)
    image = Image.fromarray(cv2_img_resized)  # 将每一帧转为Image
    image_big = Image.open(filepath)

    img_base64 = frame2base64(cv2_img_resized)

    data = {"api_key": key,
            "api_secret": secret,
            'image_base64': img_base64}

    response = requests.post(http_url, data=data)  # POTS上传
    req_con = response.content.decode('utf-8')  # response的内容是JSON格式
    content = ast.literal_eval(req_con)

    (min_left_ratio, max_right_ratio, min_top_ratio, max_bottom_ratio, max_length_of_frame_ratio) \
        = frame_face(image, content)

    box_list, count = cut_image(image_big, cv2_img, min_left_ratio, max_right_ratio,
                           min_top_ratio, max_bottom_ratio, max_length_of_frame_ratio)
    student_list = box_search(image_big, cv2_img, box_list, group)
    student_list2 = sorted(set(student_list), key=student_list.index)
    print(student_list2)

    # image.save("C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\26.jpg")
    cv2.imwrite("C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\28.jpg", cv2_img)
    cv2.waitKey(0)

    t2 = (cv2.getTickCount() - t1) / cv2.getTickFrequency()
    print(t2)
    return student_list2,cv2_img


# 图片路径
# filepath = "C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\js_2_big.jpg"  # 原图图片文件的绝对路径
# attendance_system(filepath)