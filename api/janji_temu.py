from . import api
from .janji_temu import JanjiTemu
from .users import Users
from .dokter import Dokter
from config import db
from flask import jsonify, request

@api.route('/janji_temu', methods=['GET'])
def get_janji_temu():
    janji_temu = db.session.query(JanjiTemu).all()
    if janji_temu:
        data = [j.json() for j in janji_temu]
        return jsonify(data)
    else:
        return jsonify({'message': 'Tidak ada janji temu'})

@api.route('/janji_temu/<id>', methods=['GET'])
def get_janji_temu_by_id(id):
    janji_temu = db.session.query(JanjiTemu).filter_by(id=id).first()
    if janji_temu:
        return jsonify(janji_temu.json())
    else:
        return jsonify({'message': 'Janji temu tidak ditemukan'})

@api.route('/janji_temu', methods=['POST'])
def add_janji_temu():
    nama = request.json['nama']
    tanggal = request.json.get('tanggal')
    id_user = request.json.get('id_user')
    id_dokter = request.json.get('id_dokter')

    try:
        janji_temu = JanjiTemu(nama=nama, tanggal=tanggal, id_user=id_user, id_dokter=id_dokter)
        db.session.add(janji_temu)
        db.session.commit()
        return jsonify({'message': 'Janji temu berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan janji temu', 'error': str(e)})

@api.route('/janji_temu/<id>', methods=['PUT'])
def update_janji_temu(id):
    janji_temu = db.session.query(JanjiTemu).filter_by(id=id).first()
    if not janji_temu:
        return jsonify({'message': 'Janji temu tidak ditemukan'})

    janji_temu.nama = request.json.get('nama', janji_temu.nama)
    janji_temu.tanggal = request.json.get('tanggal', janji_temu.tanggal)
    janji_temu.id_user = request.json.get('id_user', janji_temu.id_user)
    janji_temu.id_dokter = request.json.get('id_dokter', janji_temu.id_dokter)

    try:
        db.session.commit()
        return jsonify({'message': 'Janji temu berhasil diperbarui'})
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui janji temu', 'error': str(e)})

@api.route('/janji_temu/<id>', methods=['DELETE'])
def delete_janji_temu(id):
    janji_temu = db.session.query(JanjiTemu).filter_by(id=id).first()
    if not janji_temu:
        return jsonify({'message': 'Janji temu tidak ditemukan'})

    try:
        db.session.delete(janji_temu)
        db.session.commit()
        return jsonify({'message': 'Janji temu berhasil dihapus'})
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus janji temu', 'error': str(e)})
