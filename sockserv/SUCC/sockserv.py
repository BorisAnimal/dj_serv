import hashlib as hl
import json
import pickle
import time
from socket import *
from threading import Thread

import requests

host = '127.0.0.1'
djhost = '10.240.22.236'
djport = 8000
port = 26464
buf = 4096
curCon = {}


def unzip(x):
    return list(zip(*x))


def CHECK_USER(log, pas):
    headers = {'Content-type': 'application/json'}
    res = requests.post('http://{}:{}/users/check/'.format(djhost,djport), data=json.dumps({"username":log,"password":pas}),headers=headers).json()
    print(res)
    return 'token' in res


def get_applet_id(login: str):
    return hl.sha1((login + str(time.time()) + 'flaKK>DJang0').encode()).hexdigest()


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
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class HandlerThread(Thread):
    def __init__(self, tuple):
        client_socket = tuple[0]
        address = tuple[-1]
        Thread.__init__(self)
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
            self.client.close()
            print("Applet {} disconnected , now curCon is {}".format(self.hostname,curCon))
            pass


class Initializer:
    def run(self):
        print("Socket server starting")
        addr = (host, port)
        succ = socket()
        succ.bind(addr)
        succ.listen(8)
        print('Server started')
        while True:
            try:
                h = HandlerThread(succ.accept())
                print("{} connected, client = {}, address = {}".format(h.address, h.client is not None, h.address))
                print("CurCon is {} now".format(curCon))
            except CheckFailedException as e:
                print("User check failed with login = {}, password = {}".format(e.errors['log'], e.errors['log']))
            else:
                h.start()