import requests

url=f"http://192.168.3.15:5000/qycx"
data={'qyname': '四川合鑫力建筑工程有限公司'}
con=requests.post(url,data=data).content.decode('gbk')
print('f')