import hashlib

class Integrity:
    def checkSum(msg):
        hashFunc = hashlib.sha256()
        hashFunc.update(msg.encode())
        hash_value = hashFunc.hexdigest()
        return hash_value
    def EncryptMessages(msg,key):
        pass
        