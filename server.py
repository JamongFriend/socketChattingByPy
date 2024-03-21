# 서버 클래스
# 소캣을 이용하여 연결
# 스레드를 이용하여 클라이언트와 클라이언트 연결
# 서도 다른 클라이언트가 연결되면 대화 시작
# 클라이언트로 부터 exit 문자열이 올때까지 계속 수신
# exit 문자열을 수신하면 while 문 탈출하여 연결종료

from socket import *    
from select import *
from threading import Thread, Event
import os
import sys

from service import Service

event = Event()  # 키보드 입력받으면 키보드 종료시키기 위한 이벤트 

HOST = ''
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 연결된 client의 소켓 집합 set of connected client sockets
clientSockets = {}

class Server:
    def __init__(self):
        self.service = Service()

    def msg_proc(self, cs, m):
        global clientSockets
        print(m)
        tokens = m.split(':')
        code = tokens[0]
        try:
            if (code.upper() == "REG"):
                id = tokens[1]
                pw = tokens[2]
                username = tokens[3]
                self.service.register(id, pw, username)
                cs.send("Success Register".encode())
                return True
            elif (code.upper() == "LOG"):
                id = tokens[1]
                pw = tokens[2]
                self.service.login(id, pw)
                cs.send("Success Login".encode())
                return True
            elif (code.upper()  == "TO"):        
                fromID = tokens[1]
                toID = tokens[2]
                toMsg = tokens[3]
                print(f"1to1: From {fromID} To {toID} Message {toMsg}") 
                toSocket = clientSockets.get(toID)
                toSocket.send(m.encode())
                cs.send("Success:1to1".encode())
                return True
            elif (code.upper()  == "QUIT"):
                fromID = tokens[1]
                self.service.logout()
                print("Disconnected:", fromID)
                return False
        except Exception as e:
            print(f"Error:{e}")
            
    def client_com(self, cs):
        # 클라이언트로부터 id 메시지를 받음

        while True:
            if event.is_set(): # event 발생하면 스레드 종료
                return
            try:  # 아래 문장 무조건 실행
                msg = cs.recv(BUFSIZE).decode()
                #print('recieve data : ',msg)
            except Exception as e:  # 위 문장 에러 처리: client no longer connected
                print(f"Error:{e}")
                clientSockets.pop(cs)
            else:  # recv 성공하면 메시지 처리
                if ( self.msg_proc(cs, msg) == False):
                    break  # 클라이언트가 종료하면 루프 탈출 후 스레드 종료

    def client_acpt(self):
        # 소켓 생성
        global serverSocket 
        serverSocket = socket(AF_INET, SOCK_STREAM) 

        # 소켓 주소 정보 할당
        serverSocket.bind(ADDR)

        # 연결 수신 대기 상태
        serverSocket.listen(10)
        print('대기')

        # 연결 수락
        while True:
            if event.is_set(): # event 발생하면 스레드 종료
                return
            clientSocket, addr_info = serverSocket.accept()
            print('연결 수락: client 정보 ', addr_info)
            tc = Thread(target = self.client_com, args=(clientSocket,))
            tc.daemon = True
            tc.start()

ser = Server()

ta = Thread(target=ser.client_acpt)
ta.daemon = True
ta.start()

msg = input()
if msg.upper() == "Q":
    event.set()
# 소켓 종료

for socket in clientSockets.values():
    try:
        socket.shutdown()
        socket.close()
    except Exception as e:
        continue
    
serverSocket.close()
print('종료')