#데이터 베이스 클래스

import pymysql
from member import Member

class DBfunc:
    def __init__(self):
        self.conn = None

    # Mysql workbench 연결
    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root',password='83492761',db='NetworkAccount', charset='utf8')
    
    # 연결종료
    def closeconn(self):
        self.conn.close()

    def insert(self, a:Member):
        self.connect() #db연결
        cur = self.conn.cursor() #커서 객체 생성
        sql = 'insert into account (id, pw, username) values(%s, %s, %s)' #sql문
        d =  (a.id, a.pw, a.username) # %s의 각 자리에 들어갈 값을 튜플로 정의
        cur.execute(sql, d) #sql문 실행 
        self.conn.commit() # mysql 커밋
        self.closeconn()
    
    def select(self, id:str):
        try:
            self.connect()  #db연결
            cur = self.conn.cursor() #커서 객체 생성
            sql = 'select * from account where id=%s' #sql문
            dbid =  (id,) # id값
            cur.execute(sql, dbid) #sql문 실행 
            row = cur.fetchone()  # 현제 커서 위치의 한줄 추출
            if row:
                return Member(row[0], row[1], row[2])
        except Exception as e:
            print(e)
        finally:
            self.closeconn()