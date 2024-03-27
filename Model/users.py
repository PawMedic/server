from werkzeug.security import generate_password_hash
from config import db
from datetime import date


def getNomerUser():
    now = date.today()
    bk = db.session.query(Users).order_by(Users.id.desc()).first()
    if bk:
        no = int(bk.id[-3:]) + 1
        return f'UR{now.strftime("%y%m%d")}{no:03d}'
    else:
        return f'UR{now.strftime("%y%m%d")}{1:03d}'

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(11), primary_key=True, default=getNomerUser)
    nama = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(162), nullable=False)
    telepon = db.Column(db.String(13), nullable=False)
    level = db.Column(db.String(7), nullable=False, default='user')

    def __init__(self, nama:str, username:str, password:str, telepon:str, level:str=None):
        self.id = getNomerUser()
        self.nama = nama
        self.username = username
        self.password = generate_password_hash(password) 
        self.telepon = telepon
        if level is not None:
            self.level = level 
        else:
            self.level = 'user' 

    def json(self):
        return {
        'id' : self.id,
        'nama' : self.nama,
        'username' : self.username,
        'password' : self.password,
        'telepon' : self.telepon,
        'level' : self.level,
        }