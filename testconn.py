import requests
import numpy as np
import base64
import json

url1 = 'http://118.24.26.162:5000/device/register.do'
url2 = 'http://118.24.26.162:5000/face/add.do'
url3 = 'http://118.24.26.162:5000/face/find_detection.do'
url4 = 'http://118.24.26.162:5000/task/list.do'
url5 = 'http://118.24.26.162:5000/face/find_user.do'

'''
binary_img_list = args['binary_img_list']
sn = args['sn']
user_id = args['user_id']
user_name = args['user_name']
     user_id = args['user_id']
        sn = args['sn']
'''
#
url8 = 'http://118.24.26.162:5000/task/delete.do'
data = {"sn": "abc", "cam_url": "114.11.11.11:5120/cam/url/three"}
response = requests.post(url=url8, data=data)
print(response.status_code)
print(response.text)

# #将图片数据转成base64格式
# with open('/root', 'rb') as f:
#     img = base64.b64encode(f.read()).decode()
# image = []
# image.append(img)
# res = {"image":image}
# #访问服务
# _ = requests.post("http://10.0.0.160:5005",data=res)
# data = {"sn": "abc", "img_register": image}

#
# url2 = 'http://118.24.26.162:5000/face/register.do'
# with open(r"/home/centos/Downloads/webService/saveimg/register_face_6.jpg", "rb") as f:  # 转为二进制格式
#     img = base64.b64encode(f.read()).decode()    # 转base64
#     image = json.dumps(img)                      # 使用json格式
#     data = {"sn": "abc", "user_name": "liwanga", "user_id": "3456", "binary_img_list": image}
#     response = requests.post(url=url2, data=data)
#     print(response.status_code)
#     print(response.text)

# url5 = 'http://118.24.26.162:5000/face/find_detection.do'
# with open(r"/home/centos/Downloads/webService/saveimg/register_face_6.jpg", "rb") as f:  # 转为二进制格式
#     img = base64.b64encode(f.read()).decode()  # 转base64
#     image = json.dumps(img)  # 使用json格式
#     data = {"sn": "abc", "img_register": image}
#     response = requests.post(url=url5, data=data)
#     print(response.status_code)
#     print(response.text)
