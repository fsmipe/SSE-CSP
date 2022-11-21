import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher:

    def __init__(self, keySeed1, keySeed2):
        self.skey = hashlib.sha256(keySeed1.encode()).digest()
        self.TAkey = hashlib.sha256(keySeed2.encode()).digest()

    def encrypt(self, data):
        data = self.pad(data)
        iv = Random.new().read(16)
        cipher = AES.new(self.skey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(data.encode()))

    def decrypt(self, encData):
        encData = base64.b64decode(encData)
        iv = encData[:16]
        cipher = AES.new(self.skey, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(encData[16:])).decode('utf-8')

    def pad(self, s):
        return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def getTAkey(self):
        return self.TAkey
