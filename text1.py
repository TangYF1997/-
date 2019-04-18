#!/usr/bin/python
# -*- coding: utf-8 -*-

# 引入云API入
import QcloudApi

'''
module 设置需要加载的模块
已有的模块列表：
cvm      对应   cvm.api.qcloud.com
cdb      对应   cdb.api.qcloud.com
lb       对应   lb.api.qcloud.com
trade    对应   trade.api.qcloud.com
sec      对应   csec.api.qcloud.com
image    对应   image.api.qcloud.com
monitor  对应   monitor.api.qcloud.com
cdn      对应   cdn.api.qcloud.com
'''
module = 'sec'

'''
action 对应接口的接口名，请参考wiki文档上对应接口的接口名
'''
action = 'CaptchaQuery'

config = {
    'Region': 'iai.tencentcloudapi.com',
    'secretId': 'AKIDhBjdxFekXujPwJPFzZzM1EkpgYBcKtjd',
    'secretKey': 'MRbWJp6PWOEsJSwlWsACSvMXR56rRkGo',
    'method': 'get'
}

'''
params 请求参数，请参考wiki文档上对应接口的说明
'''
params = {
    'userIp': '10.0.0.1',
    'businessId': 1,
    'captchaType': 1,
    'script': 0,
    # 'Region': 'gz',当Region不是上面配置的DefaultRegion值时，可以重新指定请求的Region
    # 'SignatureMethod':'HmacSHA256',指定所要用的签名算法，可选HmacSHA256或HmacSHA1，默认为HmacSHA1
}

try:
    service = QcloudApi(module, config)

    # 请求前可以通过下面四个方法重新设置请求的secretId/secretKey/region/method参数
    # 重新设置请求的secretId
    secretId = 'AKIDhBjdxFekXujPwJPFzZzM1EkpgYBcKtjd'
    service.setSecretId(secretId)
    # 重新设置请求的secretKey
    secretKey = 'MRbWJp6PWOEsJSwlWsACSvMXR56rRkGo'
    service.setSecretKey(secretKey)
    # 重新设置请求的region
    region = 'sh'
    service.setRegion(region)
    # 重新设置请求的method
    method = 'post'
    service.setRequestMethod(method)

    # 生成请求的URL，不发起请求
    print
    service.generateUrl(action, params)
    # 调用接口，发起请求
    print
    service.call(action, params)
except Exception as e:
    print ('exception:',e)