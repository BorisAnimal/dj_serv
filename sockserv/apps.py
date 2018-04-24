from django.apps import AppConfig
import pickle, time
import hashlib as hl
from socket import *
from threading import Thread

from django.contrib import auth

class SockservConfig(AppConfig):
    name = 'sockserv'

    def ready(self):
    	print("HEllo from sockets!")
    	Thread(target=Initializer().run).start()
    	print("Socket server runned")
    	


host = 'localhost'
port = 26464
buf = 4096
curCon = {}


def unzip(x):
    return list(zip(*x))


def CHECK_USER(log, pas):
    # TODO by BORIAN
    user = auth.authenticate(username=log, password=pas)
    if user is None:
    	return False
    else:
    	return True


def get_applet_id(login: str):
    return hl.sha1((login + str(time.time()) + 'flaKK>DJang0').encode()).hexdigest()


# NONCHECKED
def send_data(id, ADlog, ADpas):
    curCon[id][-1].send(pickle.dumps({"log": ADlog, "pas": ADpas}))


def accept_connection(login, ip, hostname, sock):
    key = get_applet_id(login)
    curCon[key] = (login, ip, hostname, sock)
    return key


def getlist(login):
    print("collecting list")
    try:
        a = list(filter(lambda x: x[-1][0] == login, curCon.items()))
    except IndexError:
        return []
    ret = []
    for entry in a:
        dict = {}
        dict['id'] = entry[0]
        dict['description'] = entry[1][2]
        ret.append(dict)
    return ret


class CheckFailedException(Exception):
    def init(self, message, errors):
        super().init(message)
        self.errors = errors


class HandlerThread(Thread):
    def init(self, tuple):
        client_socket = tuple[0]
        address = tuple[-1]
        Thread.init(self)
        dict = pickle.loads(client_socket.recv(buf))
        self.client = client_socket
        self.address = address
        self.password = dict['password']
        self.login = dict['login']
        self.hostname = dict['hostname']
        if CHECK_USER(self.login, self.password) is False:
            raise CheckFailedException('User check failed', {"log": self.login, "pas": self.password})
        else:
            self.cid = accept_connection(self.login, self.address, self.hostname, self.client)
            print(
                "{}'d handler created with id {} having login {} and password {}".format(self.address, self.cid, dict['login'],
                                                                                         dict['password']))

    def run(self):
        try:
            while True:
                print("Client {} sent: {}".format(self.hostname,self.client.recv(1024)))
        except ConnectionResetError:
            pass
        finally:
            curCon.pop(self.cid)
            self.client.shutdown()
            self.client.close()
            print("Applet {} disconnected , now curCon is {}".format(self.hostname,list(curCon.items())))
            pass


class Initializer:
    def run(self):
        print("Socket server starting")
        addr = (host, port)
        succ = socket()
        succ.bind(addr)
        succ.listen(8)
        while True:
            try:
                h = HandlerThread(succ.accept())
                print("{} connected, client = {}, address = {}".format(h.address, h.client is not None, h.address))
                print("CurCon is {} now".format(list(curCon.items())))
            except CheckFailedException as e:
                print("User check failed with login = {}, password = {}".format(e.errors['log'], e.errors['log']))
            else:
                h.start()
        succ.shutdown()
        succ.close()

