from socket import *
from pynput.keyboard import Controller
import pickle, time
import hashlib, os
from cryptota import AESDecryptor as ad


class Applet:
    def init(self):
        self.host = '127.0.0.1'
        self.port = 26464
        self.buf = 4096
        self.log = hashlib.sha256('guru'.encode()).hexdigest()
        self.paswd = hashlib.sha256('ruru'.encode()).hexdigest()
        self.addr = (self.host, self.port)
        self.kb = Controller()
        self.sock = socket()
        self.decr = ad('ruru', 100000)

    def OUT(self, str):
        print(str)

    def start(self):
        while True:
            try:
                self.sock.connect(self.addr)
                break
            except ConnectionRefusedError:
                self.OUT("Connection refused. Will try again in 5 seconds...")
                time.sleep(5)
        self.sock.send(pickle.dumps({"login": self.log, "password": self.paswd, "hostname": gethostname()}))
        while self.sock:
            try:
                query = pickle.loads(self.sock.recv(self.buf))
            except ConnectionResetError:
                self.sock.close()
                self.OUT('Server shutdown. Closing app in 5 seconds...')
                time.sleep(5)
                os._exit(-4)
            except EOFError:
                self.sock.close()
                self.OUT('Wrong login or password. Closing app in 5 seconds...')
                time.sleep(5)
                os._exit(-8)
            self.autotype(query['log'], query['pas'])

    def autotype(self, l, p):
        self.OUT("5 sec, then print log, then 0.5 sec then pass")
        l, p = self.decr.decrypt(l), self.decr.decrypt(p)
        time.sleep(5)
        for x in l:
            self.kb.press(x)
            self.kb.release(x)
        time.sleep(0.5)
        for x in p:
            self.kb.press(x)
            self.kb.release(x)


if name == 'main':
    Applet().start()