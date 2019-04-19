import urllib.request as urllib2
import base64


'''
人脸注册
输入图像路径，根据学生id和学生所在的组（可以是班级，也可以是课程）将图片载入人脸库的固定位置
'''


def add_face(filepath, user_id, group_id, user_info):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"

    with open(filepath, "rb") as fp:
        base64_data = base64.b64encode(fp.read())
    img_base64_utf_8 = str(base64_data, 'utf-8')

    params = "{\"image\":\"" + img_base64_utf_8 + " \",\"image_type\":\"BASE64\",\"group_id\":\""+group_id+"\",\"user_id\":\""+user_id+"\",\"user_info\":\"\",\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\",\"action_type\":\"REPLACE\"}"
    # params = "{\"image\":\"" + img_base64_utf_8 + " \",\"image_type\":\"BASE64\",\"group_id\":\""+group_id+"\",\"user_id\":\"8\",\"user_info\":\""+user_info+"\",\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\",\",\"action_type\":\"REPLACE \"}"
    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))  # 将数据编成utf—8格式传送
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")  # 将信息解码后读取
    if content:
       print(content)


# '''
# 利用for循环输入64张人脸，有部分由于各种原因不能输入
# 1.图片人脸残缺
# 2.图片检测不出人脸
# 3.api使用受到限制
# '''
# for i in range(2, 64):
#     filepath = 'C:\\Users\\Administrator\\Pictures\\大教室2\\' + str(i) + '.jpg'
#     add_face(filepath,str(i),"DX1503","")


def update_face(filepath, user_id, group_id, user_info):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/update"

    with open(filepath, "rb") as fp:
        base64_data = base64.b64encode(fp.read())
    img_base64_utf_8 = str(base64_data, 'utf-8')

    params = "{\"image\":\"" + img_base64_utf_8 + " \",\"image_type\":\"BASE64\",\"group_id\":\""+group_id+"\",\"user_id\":\""+user_id+"\",\"user_info\":\"\",\"quality_control\":\"NONE\",\"liveness_control\":\"NONE\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))  # 将数据编成utf—8格式传送
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")  # 将信息解码后读取
    if content:
       print(content)


'''
人脸更新函数，根据输入的学生学号和所在组的名称，将该学生的人脸库中的照片全部替换为输入的图片
'''

i = 22
filepath = 'C:\\Users\\Administrator\\Pictures\\大教室2\\' + str(i) + '.jpg'
update_face(filepath, str(i), "DX1503", "")

