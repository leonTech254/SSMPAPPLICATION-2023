import hashlib
import base64
import random
class Integrity:
    def checkSum(msg):
        hashFunc = hashlib.sha256()
        hashFunc.update(msg.encode())
        hash_value = hashFunc.hexdigest()
        return hash_value
    def EncryptMessages(msg,key):
        pass
    
    def generate_key(length):
        code=""
        for i in range(0,length):
            code+=str(random.randint(0,9))
        return code    
class Encryption:
    # Encryption
    def encrypt(key, message):
        cipher = []
        for i, c in enumerate(message):
            key_c = ord(key[i % len(key)])
            msg_c = ord(c)
            cipher.append(chr((msg_c + key_c) % 127))
        return base64.urlsafe_b64encode("".join(cipher).encode()).decode()

    # Decryption
    def decrypt(key, message):
        message = base64.urlsafe_b64decode(message).decode()
        plain = []
        for i, c in enumerate(message):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            plain.append(chr((enc_c - key_c) % 127))
        return "".join(plain)

    # key = generate_key(length=8)
    # message = "Hello World"
    # encrypted_message = encrypt(key, message)
    # decrypted_message = decrypt(key, encrypted_message)
    # print(decrypted_message)  # "Hello World"
