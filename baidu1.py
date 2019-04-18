import urllib.request as urllib2, sys
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=lDsbbF6YmdtpdwdjZyIz08aF&client_secret=2MBLkXYOVmGUjqPEfxKD8Wwz3lwzLSoW'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)