import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:

    def __init__(self, keySeed1, keySeed2):
        self.skey = hashlib.sha256(keySeed1.encode()).digest()
        self.TAkey = hashlib.sha256(keySeed2.encode()).digest()
        self.bs = 16
        self.iv = hashlib.sha256(self.TAkey).digest()[:16]

    def encrypt(self, raw, authority):
        raw = self._pad(raw)

        if authority == "TA":
            cipher = AES.new(self.TAkey, AES.MODE_CBC, self.iv)
        else:
            cipher = AES.new(self.skey, AES.MODE_CBC, self.iv)
        return base64.b64encode(self.iv + cipher.encrypt(raw.encode()))

    def decrypt(self, encData, authority):
        encData = base64.b64decode(encData)
        iv = encData[:16]
        if authority == "TA":
            cipher = AES.new(self.TAkey, AES.MODE_CBC, iv)
        else:
            cipher = AES.new(self.skey, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(encData[16:])).decode('utf-8')

    def pad(self, s):
        print("Before " + str(len(s)))
        s = s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        print("After " + str(len(s)))
        print()

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def getTAkey(self):
        return self.TAkey