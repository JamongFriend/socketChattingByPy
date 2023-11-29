import socket
from threading import Thread
from datetime import datetime
from pathlib import Path
from os.path import exists
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
BUF_SIZE = 1024
SEP = ":" # 클라이언트 이름과 메세지 구분

# 소켓 생성
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# 서버 연결
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

def listenMessages():
    while True:
        try:
            message = s.recv(BUF_SIZE).decode()
            
            tokens= message.split(SEP)
            code = tokens[0]
            if code.upper() == "FILE":
                received = 0
                fromID = tokens[1]
                toID = tokens[2]
                f_name = 'img/'+tokens[3]
                f_size = int(tokens[4])

                with open(f_name, 'wb') as f:         
                    try:            
                        while received < f_size: #데이터가 있을 때까지
                            data = s.recv(BUF_SIZE)                
                            f.write(data) #1024바이트 쓴다                
                            received += len(data)
                            print("FILE recieved", received)
    
                        print('파일 %s 수신:  %d bytes' %(f_name, received))
                    except Exception as ex:
                        print(ex)
            else:
                print("\n" + message)
        except Exception as e:
            print(f"Error:{e}")


t = Thread(target=listenMessages)
t.daemon = True
t.start()

myID = input("Enter your ID: ")
toMsg = "ID"+SEP+myID+SEP
s.send(toMsg.encode())

while True:
    msg =  input()
    tokens = msg.split(SEP)
    code = tokens[0]
    # a way to exit the program
    if code.upper() == 'Q':
        toMsg = "Quit"+SEP+myID+SEP
        s.send(toMsg.encode())
        break
    elif code.upper()  == "BR" :
        toMsg = code + SEP + myID + SEP + tokens[1] + SEP
        s.send(toMsg.encode())
    elif code.upper() == "TO":
        toMsg = code + SEP + myID + SEP + tokens[1] + SEP + tokens[2] + SEP
        s.send(toMsg.encode())
    elif code.upper() == "FILE":
        toID = tokens[1]
        filename = tokens[2]
        if not exists(filename):
            print("no file")
        else:
            file_size = Path(filename).stat().st_size 
            toMsg = code + SEP + myID + SEP + toID +SEP+ filename + SEP + str(file_size) + SEP
            print(toMsg)
            
            s.send(toMsg.encode())
            sent = 0
            with open(filename, 'rb') as f:
                try:
                    data = f.read(1024) #1024바이트 읽는다
                    while data: #데이터가 없을 때까지
                        sent += s.send(data) #1024바이트 보내고 크기 저장
                        data = f.read(1024) #1024바이트 읽음
                    print("Complete File tx ")
                except Exception as ex:
                    print(ex)
    toMsg = '' 


s.close()