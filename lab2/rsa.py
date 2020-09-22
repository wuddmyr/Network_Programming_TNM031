from Crypto.Util import number	

# generate random primes (1024 bits) for p and q
p = number.getPrime(1024)	
q = number.getPrime(1024)	

n = p*q

# calculate phi (q-1)*(p-1)
phi = (p-1)*(q-1)	

# generate random prime (16 bit) for e
# check if e is factor of phi, if factor generate a new prime and check
e = number.getPrime(16)	
while True:	
    if phi % e == 0:		
        e = number.getPrime(16)	
    else:	
        break	

# calulcate d, (de = 1 % phi => d = 1/e % phi)	
d = number.inverse(e, phi)	

# read message from input
message = input()
if len(message) == 0:
    exit()	

# covert message from string to number representation
text = ord(message[0])	
for m in message[1:]:	
    text = text * 1000 + ord(m)	
print("Numer rep. of input text: ", text, "\n")

# encrypt with public key (e, n)
# calculate c = m^e % n
c = pow(text, e, n)	
print("Encrypted message: ", c, "\n")

# decrypt with private key (d, n)
# calculate m = c^d % n
new_message = int(pow(c, d, n))
print("Decrypted message: ", new_message, "\n")	

# convert message from number to string representation
text = ''
while new_message != 0:
    char = new_message % 1000
    new_message //= 1000
    text = chr(char) + text
print("User input text was: ", text)