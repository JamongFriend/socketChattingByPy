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

class Menu:
    def __init__(self):
        self.user = User()

    def menu(self):
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 종료")
        msg = input(">>>")
        if msg == '1':
            toMsg = "reg"+SEP
            s.send(toMsg.encode())
        elif msg == '2':
            self.user.login()
        elif msg == '3':
            quit()

def listenMessages():
    while True:
        try:
            message = s.recv(BUF_SIZE).decode()
            print("\n" + message)
        except Exception as e:
            print(f"Error:{e}")

m = Menu()
m.menu()

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