from hashlib import pbkdf2_hmac
from binascii import unhexlify
from Crypto.Cipher import AES


class AESDecryptor:
    def __init__(self,key,iter):
        self.key = key
        self.iter =iter

    def decrypt(self, str):
        arr = unhexlify(str)
        self.a = AES.new(self.garbleString(self.key, "leaderSucciLeadsUsToVictory".encode(), self.iter, 'sha1'), AES.MODE_GCM,
                         arr[:12])
        return self.a.decrypt(arr[12:-16]).decode()

    def garbleString(self, st, salt, iterations, hash_algorithm):
        target = str.encode(st)
        return pbkdf2_hmac(hash_algorithm, target, salt, iterations, 32)