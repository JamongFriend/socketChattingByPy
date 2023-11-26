class Member:
    def __init__(self, id=None, pw=None, username=None):
        self.id = id
        self.pw = pw
        self.username = username
    
    def __str__(self):
        return 'id: '+self.id+'pw: '+self.pw+'username: '+self.username