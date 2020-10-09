import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import base64

key = RSA.generate(1024, Random.new().read) #generate pub and priv key

# generate private key
f = open('private_key.pem','wb')
f.write(key.export_key('PEM'))
f.close()

# generate public key
f = open('public_key.pem','wb')
f.write(key.publickey().export_key('PEM'))
f.close()

# f = open('private_key.pem','r')
# key2 = RSA.import_key(f.read())
# print(key2.export_key('PEM'))

# f = open('public_key.pem','r')
# key3 = RSA.import_key(f.read())
# print(key3.export_key('PEM'))

# print(key2.export_key('PEM'))
# print(key3.export_key('PEM'))
f = open('test.txt', 'rb')
f = f.read()
print(f)

cipher = PKCS1_OAEP.new(public_key())
phn = cipher.encrypt(f)
phn = base64.b64encode(phn)
print(phn)

# b'discgolf < minipingis < fickpingis < bordshockey'
# b'Aww0AOhTPwB7Vj6T2d+3/x3yXpRHoXn5BqyD0efYq81ShRju3zFpTqLV72/X1OcUji8IVOe4EPJtD/00UaDWxVUQNN3fgsTtQVRNTRTwMzvBZ+h6XGXvHaC2RIDchFUXnmGmewSzkIBigyr4GGT5MEB56c1rSl/mmOfqeoeyV9U='
f = open('test2.txt', 'wb')
f.write(phn)
f.close()

data = open('test2.txt', 'rb')
data = data.read()
print(data)

cipher = PKCS1_OAEP.new(key)
data = base64.b64decode(data)
phn2 = cipher.decrypt(data)
print(phn2)

f = open('test3.txt', 'wb')
f.write(phn2)
f.close()

# new_file = key.publickey().encrypt(f, 'x')
# print('encrypted message', new_file)




## ENCRYPT
# f = open('public_key.pem', 'rb')
# f = f.read()
# public_key = RSA.importKey(f)

# for root, dirs, files in os.walk('files'):
#     print(root, dirs, files) 

#     for filename in files:
#         print(filename)
        
#         input_file = open(root + "/" + filename, 'rb')

#         encrypted_data = b''
#         while True:
#             data = input_file.read(64)
#             if not data:
#                 break
#             block = keys.encrypt(public_key, data)
#             encrypted_data += block + b'\n'
        
#         input_file.close()
    
#         output_file = open(root + "/" + filename, 'wb')
#         output_file.write(encrypted_data)
#         output_file.close()

## DECRYPT
# f = open('private_key.pem', 'rb')
# f = f.read()
# key = RSA.importKey(f)

# for root, dirs, files in os.walk('files'):

#     for filename in files:
#         print(filename)
#         input_file = open(root + "/" + filename, 'rb')
        
#         data = input_file.read()
#         data = data.split(b'\n')
#         input_file.close()
        
#         decrypted_data = b''
#         for row in data:
#             if not row:
#                 break
#             decrypted_data += keys.decrypt(key, row)


#         #print(decrypted_data)
#         output_file = open(root + "/_" + filename, 'wb')
#         output_file.write(decrypted_data)
#         output_file.close()
      