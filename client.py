import socket
from threading import Thread
from datetime import datetime
from pathlib import Path
from os.path import exists
import sys

from service import Service

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

class Client:
    def __init__(self):
        self.Service = Service()

    def menu(self):
        while True:
            print("1. 회원가입")
            print("2. 로그인")
            print("3. 로그아웃")
            print("4. 채팅")
            msg = input(">>>")
            if msg == '1':
                id = input('ID 입력:')
                pw = input('PW 입력:')
                Servicename = input('이름 입력: ')
                toMsg = "REG"+SEP+id+SEP+pw+SEP+Servicename+SEP
                s.send(toMsg.encode())
            elif msg == '2':
                id = input('ID 입력:')
                pw = input('PW 입력:')
                toMsg = "LOG"+SEP+id+SEP+pw+SEP
                s.send(toMsg.encode())
            elif msg == '3':
                toMsg = "QUIT"+SEP+id+SEP
                s.send(toMsg.encode())
            elif msg == '4':
                chatting()

def listenMessages():
        while True:
            try:
                message = s.recv(BUF_SIZE).decode()
                print("\n" + message)
            except Exception as e:
                print(f"Error:{e}")

myID = Service.loginedAccount

def chatting():
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

c = Client()

t = Thread(target=listenMessages)
t.daemon = True
t.start()

c.menu()


s.close()