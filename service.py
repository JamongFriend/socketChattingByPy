from member import Member
from database import DBfunc

class User:
    loginedAccount = ''

    def __init__(self):
        self.DBfunc = DBfunc()

    def register(self):
        id = input('ID 입력:')
        pw = input('PW 입력:')
        username = input('이름 입력: ')
        self.DBfunc.insert(Member(id = id, pw=pw, username=username))

    def login(self):
        inputID = input('ID 입력:')
        inputPW = input('PW 입력:')
        a = self.DBfunc.select(inputID)
        
        if a==None and inputPW != a.pw:
            print("로그인 실패")
            return
        else:
            User.loginedAccount = inputID
            print("로그인 성공")
        

    def logout():
        User.loginedAccount = ''
        print('로그아웃 완료')
        return