import urllib.request
import json
import base64
import tkinter.messagebox
import ast

'''
人脸对比
'''
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
filename1 = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\faceKu\\0.png'
filename2 = 'C:\\Users\\Administrator\\PycharmProjects\\untitled\\2.jpg'
f = open(filename1, 'rb')
f2 = open(filename2, 'rb')
img_test1 = base64.b64encode(f.read())
img_test2 = base64.b64encode(f2.read())

params = json.dumps(
    [{"image": '' + str(img_test1, 'utf-8') + '', "image_type": "BASE64", "face_type": "LIVE",
      "quality_control": "LOW"},
     {"image": '' + str(img_test2, 'utf-8') + '', "image_type": "BASE64", "face_type": "IDCARD",
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
content = ast.literal_eval(content)
print(content['result']['score'])
tkinter.messagebox.showinfo('图片相似度', "两个人的相似度为：%d"%content['result']['score']+"%")