import urllib.request as urllib2
import cv2
import ast
import base64
import urllib.parse
from urllib.parse import urlencode
'''
人脸搜索
'''

request_search_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
filepath = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\0.png'
with open(filepath, "rb") as fp:
    base64_data = base64.b64encode(fp.read())
img_base64_utf_8 = str(base64_data, 'utf-8')
# print(img_base64_utf_8)
#请求参数
params = "{\"image\":\""+ img_base64_utf_8 +"\",\"image_type\":\"BASE64\",\"group_id_list\":\"DX1501\",\"quality_control\":\"LOW\",\"liveness_control\":\"NONE\"}"
access_token = '24.d4ec3047377e6ca61e27b571613df0e6.2592000.1557116267.282335-15647216'
request_url = request_search_url + "?access_token=" + access_token
request = urllib2.Request(url=request_url, data=params.encode("utf-8"))
request.add_header('Content-Type', 'application/json')
response = urllib2.urlopen(request)
content = response.read()
if content:
    print (content)
content = content.decode("utf-8")
if content[14] != '0':
    str1 = content[33:50]
    print(str1)
else:
    content = ast.literal_eval(content)
    print('学生id为' + str(content['result']['user_list'][0]['user_id']))
    print('相似度为' + str(content['result']['user_list'][0]['score']))
