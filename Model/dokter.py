from config import db
from datetime import date
from .dokter import Dokter

class Dokter(db.Model):
    __tablename__ = 'dokter'
    id = db.Column(db.String(11), primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(162), nullable=False)
    level = db.Column(db.String(7), nullable=False, default='dokter')
    telepon = db.Column(db.String(13))

    def __init__(self, id:str, nama:str, username:str, password:str, telepon:str=None):
        self.id = id
        self.nama = nama
        self.username = username
        self.password = password
        self.level = 'dokter'
        self.telepon = telepon

    def json(self):
        return {
            'id' : self.id,
            'nama' : self.nama,
            'username' : self.username,
            'password' : self.password,
            'level' : self.level,
            'telepon' : self.telepon,
        }