import requests

sockets_server = 'http://10.240.22.236:5000/sendDataToApplet'
appid = '8bab507258e2936b66e07725b7d1dfd1a055fdfc'


r = requests.post(sockets_server, data={'appletid':appid, 'login': 'keku', 'pass': 'passucks'})
print(r.text)