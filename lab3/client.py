import jks
import base64
import socket
import ssl
import textwrap

HOST = '127.0.0.1'
PORT = 1337

CERT = './LIU.cer'
PRIVATE_KEY = './key2.key'

#ks = jks.KeyStore.load('LIUkeystore.ks', '123456')
#txt = base64.b64encode(ks.private_keys['liualias'].pkey).decode('ascii')
#print(txt)

# main
if __name__ == '__main__':    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sslContext = ssl.SSLContext()
    sslContext.verify_mode = ssl.CERT_NONE
    sslConnection = sslContext.wrap_socket(server)
    sslConnection.connect((HOST, PORT))

    sslConnection.sendall(b'HEJSAN SVEJSAN...')

    while True:
        m = sslConnection.recv(1024)
        print(m)
 
    # server.listen()

    # while True:
    #     conn, addr = server.accept()
        
    #     # init ssl-context
    #     sslContext = ssl.SSLContext()
    #     sslContext.load_cert_chain(CERT, PRIVATE_KEY)
    #     print("ssl loaded?", sslContext)

    #     sslConnection = sslContext.wrap_socket(conn, server_side=True)

    #     while True:
    #         message = sslConnection.recv(4096)
    #         print(message)

