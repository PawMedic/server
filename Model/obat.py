from config import db
from datetime import date, datetime
from .pembelian import Pembelian
from .penjualan import Penjualan
from flask import current_app
import socket
import base64
import imghdr


def getKodeObat() -> str:
    now = date.today()
    ob = db.session.query(Obat).order_by(Obat.id.desc()).first()
    if ob:
        no = int(ob.id[-3:]) + 1
        return f'OB{now.strftime("%y%m%d")}{no:03d}'
    else:
        return f'OB{now.strftime("%y%m%d")}{1:03d}'

def coverName(base64_data):
    try:
        _, data = base64_data.split(',', 1)
        image_data = base64.b64decode(data)
        now = datetime.now().strftime("%y%m%d%H%M%S")
        format_type = imghdr.what(None, image_data)
        return f"{now}.{format_type}"
    except Exception as e:
        print(f"Error: {e}")
        return None

class Obat(db.Model):
    __tablename__ = 'obat'
    id = db.Column(db.String(11), primary_key=True, default=getKodeObat)
    nama = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.String(), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    gambar = db.Column(db.String(25), nullable=False)
    tanggal = db.Column(db.Date, default=date.today())
    kategori = db.relationship('Kategori_Obat', backref='obat', lazy=True) 
    transaksi = db.relationship('Detail_Transaksi', backref='obat', lazy=True) 

    def __init__(self, nama:str, deskripsi:str, harga:int, stok:int, filename):
        self.id = getKodeObat()
        self.nama = nama
        self.deskripsi = deskripsi
        self.harga = harga
        self.stok = stok
        self.gambar = coverName(filename)
   
    def getGambar(self):
        IPaddress = socket.gethostbyname(socket.gethostname())
        image_path = f"http://{IPaddress}:5432/{current_app.config['UPLOAD_FOLDER']}/{self.gambar}" 
        return image_path

    def json(self):
        return {
            'id' : self.id,
            'nama' : self.nama,
            'deskripsi' : self.deskripsi,
            'harga' : self.harga,
            'stok' : self.stok,
            'gambar' : self.getGambar(),
            'tanggal' : self.tanggal,
            'kategori' : self.getKategori(),
        }