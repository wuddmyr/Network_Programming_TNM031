from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import base64

def generate_keys():
    key = RSA.generate(1024, Random.new().read) #generate pub and priv key
    return key.publickey(), key

def encrypt(public_key, message):
    cipher = PKCS1_OAEP.new(public_key)
    e_message = cipher.encrypt(message)
    return base64.b64encode(e_message)

def decrypt(private_key, message):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(base64.b64decode(message))