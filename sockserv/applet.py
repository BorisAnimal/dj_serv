from socket import *
from pynput.keyboard import Controller
import pickle,time
import hashlib

host = '127.0.0.1'
port = 26464
buf = 4096
log = hashlib.sha256('abc'.encode()).hexdigest()
paswd = hashlib.sha256('qweee123'.encode()).hexdigest()

addr = (host, port)
kb = Controller()
sock = socket()
while True:
    try:
        sock.connect(addr)
        break
    except ConnectionRefusedError:
        print("Connection refused. Will try again in 5 seconds...")
    time.sleep(5)
sock.send(pickle.dumps({"login": log, "password": paswd, "hostname":gethostname()}))
while sock:
    query = pickle.loads(sock.recv(buf))
    l, p = query['log'], query['pas']
    print ("5 sec, then print log, then 0.5 sec then pass")
    time.sleep(5)
    for x in l:
        kb.press(x)
        kb.release(x)
    time.sleep(0.5)
    for x in p:
        kb.press(x)
        kb.release(x)