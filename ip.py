import socket

def get_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		addr = print(s.getsockname()[0])
		s.close()
		return addr
	except:
		return "127.0.0.1"

DJ_PORT = 8000
FLASK_PORT = 5000

SOCK_SERV_ADDRES = '127.0.0.1'
SOCK_SERV_PORT = 26464

