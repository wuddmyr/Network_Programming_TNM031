# pycryptodome

from Crypto.Util import number

p = number.getPrime(8)
q = number.getPrime(8)
e = 11 #number.getPrime(1024)
n = p*q

diff = (p-1)*(q-1)

while True:
    if diff % e == 0:
        pass
        #e = number.getPrime(1024)
    else:
        break
print('e choosen as', e)

# Extended Euclidean Algorith (d = e^-1 % phi), phi och e får inte ha någora gemensamma faktorer
d = number.inverse(e, diff)
print(d)

public_key = (n, e)
private_key = (p, q, d)

message = 'cat'

text = ord(message[0])
for m in message[1:]:
    text = text * 1000 + ord(m)
    
#print(len(text))
# x = 11353585903572286**6116402471153 % n
# print("X=", x)


c = (text**e) % n
print("ok?", c)


new_message = c**d % n
print(new_message)

# The multiplicative inverse of “a modulo m” exists 
# if and only if a and m are relatively prime (i.e., if gcd(a, m) = 1).