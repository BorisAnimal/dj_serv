from socket import *
from pynput.keyboard import Controller
from pynput import mouse
from threading import Thread
import pickle, time
import hashlib, os
import sys
sys.path.append(sys.path[0] + "/../..")
# print(sys.path)
from ip import SOCK_SERV_ADDRES, SOCK_SERV_PORT
from cryptota import AESDecryptor as ad


# pip install pycryptodome


class Applet:
    def __init__(self, login, password, fOUT):
        self.log = hashlib.sha256(login.encode()).hexdigest()
        self.paswd = hashlib.sha256(password.encode()).hexdigest()
        self.decr = ad(password, 100000)
        self.host = SOCK_SERV_ADDRES
        self.port = SOCK_SERV_PORT
        self.buf = 4096
        self.addr = (self.host, self.port)
        self.kb = Controller()
        self.sock = socket()
        self.OUT = fOUT


    def on_click(x, y, button, pressed):
        print('BOI')
        if button == mouse.Button.left:
            return False

    def start(self):
        while True:
            try:
                self.sock.connect(self.addr)
                break
            except ConnectionRefusedError:
                self.OUT("ERROR", "Connection refused. Will try again in 5 seconds...")
                time.sleep(5)
        self.sock.send(pickle.dumps({"login": self.log, "password": self.paswd, "hostname": gethostname()}))
        while self.sock:
            try:
                query = pickle.loads(self.sock.recv(self.buf))
            except ConnectionResetError:
                self.sock.close()
                self.OUT("ERROR", 'Server shutdown. Closing app in 5 seconds...')
                time.sleep(5)
                os._exit(-4)
            except EOFError:
                self.sock.close()
                self.OUT("ERROR", 'Wrong login or password. Closing app in 5 seconds...')
                time.sleep(5)
                os._exit(-8)
            self.OUT("Notification",
                     "Authentication data {} has arrived\nPress LMB for login autotype, and then LMB again for password autotype ".format(
                         query['descr']))
            Thread(self.autotype(query['log'], query['pas'])).start()

    def close(self):
        self.sock.close()
        os._exit(-7)

    def autotype(self, l, p):
        l, p = self.decr.decrypt(l), self.decr.decrypt(p)
        with mouse.Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except:
                pass
            for x in l:
                self.kb.press(x)
                self.kb.release(x)
        time.sleep(0.5)
        with mouse.Listener(
                on_click=self.on_click) as listener:
            try:
                listener.join()
            except:
                pass
            for x in p:
                self.kb.press(x)
                self.kb.release(x)


def OUT(self, cond, str):
    print("{}:{}".format(cond, str))


if __name__ == '__main__':
    Applet('guru', 'ruru', OUT).start()
