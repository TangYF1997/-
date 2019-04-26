import urllib.request as urllib2
import base64
null = ''

'''
1:人脸注册
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
    content = eval(content)
    if content['error_code'] != 0 :
        response_msg = content['error_msg']
    else:
        response_msg = "成功注册人脸"
    return response_msg



# '''
# 利用for循环输入64张人脸，有部分由于各种原因不能输入
# 1.图片人脸残缺
# 2.图片检测不出人脸
# 3.api使用受到限制
# '''
# for i in range(2, 64):
#     filepath = 'C:\\Users\\Administrator\\Pictures\\大教室2\\' + str(i) + '.jpg'
#     add_face(filepath,str(i),"DX1503","")


'''
2:人脸更新函数
根据输入的学生学号和所在组的名称，将该学生的人脸库中的照片全部替换为输入的图片
'''


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
    content = eval(content)
    if content['error_code'] != 0 :
        response_msg = content['error_msg']
    else:
        response_msg = "成功更新人脸"
    return response_msg



# i = 22
# filepath = 'C:\\Users\\Administrator\\Pictures\\大教室2\\' + str(i) + '.jpg'
# update_face(filepath, str(i), "DX1503", "")


'''
3：人脸删除。
删除用户的某一张人脸，如果该用户只有一张人脸图片，则同时删除用户。这里需要输学生学号，学生所在的组，以及人脸图片，所以要实现此功能可能需要先获取图像
因为百度AI文档中没有写调用例子，所以我先不写
'''


def delete_face(user_id, group_id, face_token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete"

    params = "{\"user_id\":\""+user_id+"\",\"group_id\":\""+group_id+"\",\"face_token\":\""+face_token+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0 :
        response_msg = content['error_msg']
    else:
        response_msg = "成功删除人脸"
    return response_msg


# get_user_facelist("22", "DX1502")
# delete_face("22", "DX1502", "12bb74e9bb9c51b1a729be862e988695")


'''
4：用户信息查询
输入学生的学号，获得学生所在的组和学生的信息user_info
用户组id(由数字、字母、下划线组成，长度限制48B)，如传入“@ALL”则从所有组中查询用户信息。注：处于不同组，但uid相同的用户，我们认为是同一个用户。
'''


def get_user(user_id, group_id):  # group_id如传入“@ALL”则从所有组中查询用户信息
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get"
    params = "{\"user_id\":\""+user_id+"\",\"group_id\":\""+group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = content['result']['user_list']
    return response_msg


# i = 22
# get_user(str(i), "@ALL")

'''
5：获取用户的人脸列表。
用于获取一个用户的全部人脸列表。输入学生学号，组的id，返回全部人脸以及添加时间
'''


def get_user_facelist(user_id, group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/getlist"
    params = "{\"user_id\":\""+user_id+"\",\"group_id\":\""+group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = content['result']['face_list']
    return response_msg


# i = 22
# get_user_facelist(str(i), "DX1503")


'''
6：获取某一组的用户列表。
输入组名，获取该组所有用户的学号形成的list
'''


def getusers_group(group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getusers"
    params = "{\"group_id\":\""+group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = content['result']
    return response_msg

# getusers_group("DX1503")


'''
7：复制用户。
并不是向一个指定组内添加用户，而是直接从其它组复制用户信息 如果需要注册用户，请直接使用人脸注册接口，输入用户id，所在组的id以及需要复制到的组的id
如果其他组有该用户，则会在该用户中在添加一张照片
如果没有该用户，就新建该用户
'''


def copy_user(user_id, src_group_id, dst_group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/copy"
    params = "{\"user_id\":\""+user_id+"\",\"src_group_id\":\""+src_group_id+"\",\"dst_group_id\":\""+dst_group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = "成功复制人脸"
    return response_msg

# i = 22
# copy_user(str(i), "DX1503", "DX1501")


'''
8：删除用户。
将用户从某个组中删除。输入用户id，所在组的id
'''


def delete_user(user_id, group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/delete"
    params = "{\"group_id\":\""+group_id+"\",\"user_id\":\""+user_id+"\"}"
    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = "成功删除用户"
    return response_msg


# delete_user("22", "DX1501")


'''
9：创建用户组。
创建一个空的用户组，如果该组存在，则返回错误信息，输入需要创建的组的id
'''


def add_group(group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"
    params = "{\"group_id\":\""+group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = "成功创建用户组"
    return response_msg

# add_group("DX1504")


'''
10：删除用户组。
删除用户组下所有的用户及人脸，如果组不存在 则返回错误。输入需要删除的组的id
'''


def delete_group(group_id):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/delete"
    params = "{\"group_id\":\""+group_id+"\"}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = "成功删除用户组"
    return response_msg

# delete_group("DX1504")


'''
11：组列表查询。
"{\"start\":0,\"length\":100}"，请求参数只有起始序号和结束序号，返回组的id的一个list
'''


def getlist_group():
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/getlist"

    params = "{\"start\":0,\"length\":100}"

    access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
    request_url = request_url + "?access_token=" + access_token
    request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read().decode("utf-8")
    content = eval(content)
    if content['error_code'] != 0:
        response_msg = content['error_msg']
    else:
        response_msg = content['result']
    return response_msg

# getlist_group()
