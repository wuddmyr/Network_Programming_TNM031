import jks
import base64
import socket
import ssl
import textwrap

HOST = '127.0.0.1'
PORT = 1337

CERT = './LIU.cer'
PRIVATE_KEY = './private.key'

#ks = jks.KeyStore.load('LIUkeystore.ks', '123456')
#txt = base64.b64encode(ks.private_keys['liualias'].pkey).decode('ascii')
#print(txt)

# main
if __name__ == '__main__':    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        
        # init ssl-context
        sslContext = ssl.SSLContext()
        sslContext.load_cert_chain(CERT, PRIVATE_KEY)
        print("ssl loaded?", sslContext)

        sslConnection = sslContext.wrap_socket(conn, server_side=True)

        while True:
            message = sslConnection.recv(4096)
            print(message)

        # wrap socket
      