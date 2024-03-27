from . import api
from .users import Users
from .pembelian import Penjualan
from .penjualan import Penjualan
from config import db
from flask import jsonify, request
from werkzeug.security import check_password_hash


@api.route('/user', methods=['GET'])
def user():
    users = db.session.query(Users).all()
    if users:
        data = [user.json() for user in users]
        return jsonify(data)
    else:
        return  jsonify({'message' : 'tidak ada user'})
    
@api.route('/user/<id>/remove', methods=['GET'])
def removeUser(id):
    users = db.session.query(Users).filter(Users.id == id).first()
    pembelian = db.session.query(pembelian).filter(pembelian.id_user == id).all()
    penjualan = db.session.query(penjualan).filter(penjualan.id_user == id).all()

@api.route('/user/login', methods=['POST'])
def login():
    username= request.json['username']
    password= request.json['password']
    check = db.session.query(Users).filter_by(username=username).first()
    if check and check_password_hash(check.password, password):
        return jsonify(check.json())
    else:
        return jsonify({'message' : 'login gagal'})

@api.route('/user/register', methods=['POST'])
def register():
    nama = request.json['nama']
    username= request.json['username']
    password= request.json['password']
    telepon = request.json['telepon']
    try:
        user = Users(nama=nama, username=username, password=password, telepon=telepon)
        check = db.session.query(Users).filter_by(username=username).first()
        if check:
            return jsonify({'message' : 'username tidak tersdia'})
        else:
            db.session.add(user)
            db.session.commit()
            return jsonify({'message' : 'registrasi berhasil'})
    except Exception as e:
        return jsonify({'message' : 'registrasi gagal', 'ex' : str(e), })

@api.route('/user/addpegawai', methods=['POST'])
def addPegawai():
    nama = request.json['nama']
    username= request.json['username']
    password= request.json['password']
    telepon = request.json['telepon']
    level = "pegawai"
    try:
        user = Users(nama=nama, username=username, password=password, telepon=telepon, level=level)
        check = db.session.query(Users).filter_by(username=username).first()
        if check:
            return jsonify({'message' : 'username tidak tersdia'})
        else:
            db.session.add(user)
            db.session.commit()
            return jsonify({'message' : 'registrasi berhasil'})
    except Exception as e:
        return jsonify({'message' : 'registrasi gagal', 'ex' : str(e), })