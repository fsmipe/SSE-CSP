import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# Class used to encrypt and decrypt data
class AESCipher:

    # Key storing and creation
    def __init__(self, keySeed1, keySeed2):
        self.skey = hashlib.sha256(keySeed1.encode()).digest()
        self.TAkey = hashlib.sha256(keySeed2.encode()).digest()
        self.bs = 16
        self.iv = hashlib.sha256(self.TAkey).digest()[:16]

    # encrypts data, with specific key, and method (if data is unique and ciphertexts get compared, it's not made random)
    def encrypt(self, raw, authority, rand=False):
        raw = self._pad(raw)

        iv = self.iv
        if rand:
            iv = Random.new().read(16)

        if authority == "TA":
            cipher = AES.new(self.TAkey, AES.MODE_CBC, iv)
        else:
            cipher = AES.new(self.skey, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    # decrypts data with right key
    def decrypt(self, encData, authority):
        encData = base64.b64decode(encData)
        iv = encData[:16]
        if authority == "TA":
            cipher = AES.new(self.TAkey, AES.MODE_CBC, iv)
        else:
            cipher = AES.new(self.skey, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(encData[16:])).decode('utf-8')

    # normal data padding
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    # normal data unpadding
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
