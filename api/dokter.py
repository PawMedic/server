from . import api
from .dokter import Dokter
from config import db
from flask import jsonify, request
from werkzeug.security import check_password_hash

@api.route('/dokter', methods=['GET'])
def get_dokter():
    dokter = db.session.query(Dokter).all()
    if dokter:
        data = [d.json() for d in dokter]
        return jsonify(data)
    else:
        return jsonify({'message': 'Tidak ada dokter'})

@api.route('/dokter/<id>', methods=['GET'])
def get_dokter_by_id(id):
    dokter = db.session.query(Dokter).filter_by(id=id).first()
    if dokter:
        return jsonify(dokter.json())
    else:
        return jsonify({'message': 'Dokter tidak ditemukan'})

@api.route('/dokter', methods=['POST'])
def add_dokter():
    nama = request.json['nama']
    username = request.json['username']
    password = request.json['password']
    telepon = request.json['telepon']
    level = request.json.get('level', 'user')  # Default level to 'user' if not provided

    try:
        dokter = Dokter(nama=nama, username=username, password=password, telepon=telepon, level=level)
        db.session.add(dokter)
        db.session.commit()
        return jsonify({'message': 'Dokter berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan dokter', 'error': str(e)})

@api.route('/dokter/<id>', methods=['PUT'])
def update_dokter(id):
    dokter = db.session.query(Dokter).filter_by(id=id).first()
    if not dokter:
        return jsonify({'message': 'Dokter tidak ditemukan'})

    dokter.nama = request.json.get('nama', dokter.nama)
    dokter.username = request.json.get('username', dokter.username)
    dokter.password = request.json.get('password', dokter.password)
    dokter.telepon = request.json.get('telepon', dokter.telepon)
    dokter.level = request.json.get('level', dokter.level)

    try:
        db.session.commit()
        return jsonify({'message': 'Dokter berhasil diperbarui'})
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui dokter', 'error': str(e)})

@api.route('/dokter/<id>', methods=['DELETE'])
def delete_dokter(id):
    dokter = db.session.query(Dokter).filter_by(id=id).first()
    if not dokter:
        return jsonify({'message': 'Dokter tidak ditemukan'})

    try:
        db.session.delete(dokter)
        db.session.commit()
        return jsonify({'message': 'Dokter berhasil dihapus'})
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus dokter', 'error': str(e)})
