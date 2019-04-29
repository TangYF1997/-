# encoding:utf-8
import base64,cv2
import numpy as np
import urllib
import urllib.request as urllib2
import matplotlib.pyplot as plt

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