#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):
 
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
 
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
 
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
 
    def _pad(self, s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
 
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


# BS = 16
# 
# 
# def pad(s):
#     return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
# 
# 
# def unpad(s):
#     return s[0:-s[-1]]
# 
# 
# class AESCipher:
# 
#     def __init__(self, key):
#         self.key = hashlib.sha256(key.encode('utf-8')).digest()
# 
#     def encrypt(self, raw):
#         raw = pad(raw)
#         iv = Random.new().read(AES.block_size)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return base64.b64encode(iv + cipher.encrypt(raw))
# 
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         iv = enc[:16]
#         cipher = AES.new(self.key, AES.MODE_CBC, iv)
#         return unpad(cipher.decrypt(enc[16:]))
