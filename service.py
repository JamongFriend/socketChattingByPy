# 로그인, 회원가입, 로그아웃 서비스 클래스
# 회원가입을 통해 데이터베이스에 아이디, 비밀번호, 닉네임을 저장
# 로그인 시 데이터베이스에 저장되어있는 아이디와 매개변수에 입력된 아이디를 비교
# 일치할 시 비밀번호를 비교 후 다르면 실패 같으면 성공

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