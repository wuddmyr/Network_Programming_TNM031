# server
# connection with client
# store public and private key 
# store a super secret passowrd to get private key

import socket
import threading
import keys
import time
import random

HOST = '127.0.0.1'
PORT = 1337



def handler(client_socket):
    
    while True:
        msg = 'ENCRYPT'
        client_socket.sendall(msg.encode('utf-8'))
        
        public_key, private_key = keys.generate_keys()
        payload = bytes(public_key.export_key('PEM'))
        client_socket.sendall(payload)

        time.sleep(30)

        # msg = '____ENCRYPT'
        # client_socket.sendall(msg.encode('utf-8'))
        # time.sleep(5)
    


    # f = open('private_key.pem', 'wb')
    # f.write(private_key.export_key('PEM'))
    # f.close()

    # f = open('public_key.pem', 'wb')
    # f.write(public_key.export_key('PEM'))
    # f.close()

    # # payload = bytes(public_key.export_key('PEM'))
    # # client_socket.sendall(payload)
    



# main
if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        print('NEW CONNECTION:', addr)
        new_thread = threading.Thread(target=handler, args=(conn,))
        new_thread.start()