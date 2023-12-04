import socket
from threading import Thread
from datetime import datetime
from pathlib import Path
from os.path import exists
import sys

from service import User

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

def main():
    print("1. 회원가입")
    print("2. 로그인")
    print("3. 종료")
    userInput = input()
    if userInput == 1:
        User.register()
        main()
    elif userInput == 2:
        User.login()
    elif userInput == 3:
        exit()

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

main()

t = Thread(target=listenMessages)
t.daemon = True
t.start()

myID = User.loginedAccount
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
    elif code.upper() == "TO":
        toMsg = code + SEP + myID + SEP + tokens[1] + SEP + tokens[2] + SEP
        s.send(toMsg.encode())
    toMsg = '' 


s.close()