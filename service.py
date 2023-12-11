from member import Member
from database import DBfunc

class Service:
    loginedAccount = ''

    def __init__(self):
        self.DBfunc = DBfunc()

    def register(self, id, pw, username):
        self.DBfunc.insert(Member(id = id, pw=pw, username=username))

    def login(self, id, pw):
        inputID = id
        inputPW = pw
        a = self.DBfunc.select(inputID)
        
        if a==None and inputPW != a.pw:
            print("로그인 실패")
            return
        else:
            Service.loginedAccount = inputID
            print("로그인 성공")
        

    def logout():
        Service.loginedAccount = ''
        print('로그아웃 완료')
        return