import urllib.request as urllib2, sys
import ssl

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Ixv7fEgwUbnZTeXQUxPSawZn&client_secret=dIydQS4C7q9OrWaGY9hK3aR8RikHcHye'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)