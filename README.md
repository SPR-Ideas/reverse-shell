# _**REVERSE SHELL** (python)_

## **Reverse Shell :**
A reverse shell is a type of shell in which the target machine communicates back to the attacking machine. The attacking machine has a listener port on which it receives the connection, which by using, code or command execution is achieved.

### **Short description of the program:**
One has to run the `client.py` in the victims PC. This script will open a port for you to acess the victims shell with root permission. <br>
provided the attacker should give his public ip and specfic port of your router to send the information , it should be changed in `client.py `
line number 10 and 11 **assign your public IP to variabel IP and port to variabel PORT**
```Python 
IP = "localhost" #give your public ip
PORT = 9000 #give specific portof your router
```
next to that ,There is an another thing that the client pc should have the **openCV module** installed , To do that so,<br>
## **LINUX**
>pip3 install opencv-python
## **WINDOWS**
>pip install opencv-python

**NOW** ,it ready to run it in victims machine.
onces the client started it waits for attacker to run `server.py` file in attckers machine at once they get connected the attackers gets  **Reverse-TCp connection** 

## **FEATURES OF THIS FILE**
1.  attacker can download the file form victim
#### **syntax**
> download - filename
2. attacker can upload file to victim.
#### **syntax**
> upload - filename

3. attacker can acess the web-cam of the victim 
#### **syntax**
> livecam

---
if any doubts regarding runing the code ping me in the commment section
