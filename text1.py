import ast
null = ''

content = '{"error_code":222207,"error_msg":"match user is not found","log_id":304569259055899701,"timestamp":1555905590,"cached":0,"result":null}'
content = eval(content)
print(content)