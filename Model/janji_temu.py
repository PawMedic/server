from config import db
from datetime import date
from .janji_temu import Janji_Temu

def getNomerJanjiTemu():
    now = date.today()
    janji = db.session.query(JanjiTemu).order_by(JanjiTemu.id.desc()).first()
    if janji:
        no = int(janji.id[-3:]) + 1
        return f'JT{now.strftime("%y%m%d")}{no:03d}'
    else:
        return f'JT{now.strftime("%y%m%d")}{1:03d}'

class JanjiTemu(db.Model):
    __tablename__ = 'janji_temu'
    id = db.Column(db.String(11), primary_key=True, default=getNomerJanjiTemu)
    nama = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.Date, default=date.today())
    id_user = db.Column(db.String(11), db.ForeignKey('users.id'), nullable=False)
    id_dokter = db.Column(db.String(11), db.ForeignKey('dokter.id'), nullable=False)

    def __init__(self, nama:str, id_user:str, id_dokter:str, tanggal:date=None):
        self.id = getNomerJanjiTemu()
        self.nama = nama
        if tanggal is not None:
            self.tanggal = tanggal
        else:
            self.tanggal = date.today()
        self.id_user = id_user
        self.id_dokter = id_dokter

    def json(self):
        return {
            'id' : self.id,
            'nama' : self.nama,
            'tanggal' : self.tanggal,
            'id_user' : self.id_user,
            'id_dokter' : self.id_dokter,
        }