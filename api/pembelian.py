from . import api
from .pembelian import Pembelian
from config import db
from flask import jsonify, request
from datetime import date

@api.route('/pembelian', methods=['GET'])
def get_pembelian():
    pembelian = db.session.query(Pembelian).all()
    if pembelian:
        data = [p.json() for p in pembelian]
        return jsonify(data)
    else:
        return jsonify({'message': 'Tidak ada data pembelian'})

@api.route('/pembelian/<kode>', methods=['GET'])
def get_pembelian_by_kode(kode):
    pembelian = db.session.query(Pembelian).filter_by(kode=kode).first()
    if pembelian:
        return jsonify(pembelian.json())
    else:
        return jsonify({'message': 'Pembelian tidak ditemukan'})

@api.route('/pembelian', methods=['POST'])
def add_pembelian():
    kode = request.json['kode']
    tanggal = request.json['tanggal']

    try:
        pembelian = Pembelian(kode=kode, tanggal=tanggal)
        db.session.add(pembelian)
        db.session.commit()
        return jsonify({'message': 'Pembelian berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan pembelian', 'error': str(e)})

@api.route('/pembelian/<kode>', methods=['PUT'])
def update_pembelian(kode):
    pembelian = db.session.query(Pembelian).filter_by(kode=kode).first()
    if not pembelian:
        return jsonify({'message': 'Pembelian tidak ditemukan'})

    pembelian.tanggal = request.json.get('tanggal', pembelian.tanggal)

    try:
        db.session.commit()
        return jsonify({'message': 'Pembelian berhasil diperbarui'})
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui pembelian', 'error': str(e)})

@api.route('/pembelian/<kode>', methods=['DELETE'])
def delete_pembelian(kode):
    pembelian = db.session.query(Pembelian).filter_by(kode=kode).first()
    if not pembelian:
        return jsonify({'message': 'Pembelian tidak ditemukan'})

    try:
        db.session.delete(pembelian)
        db.session.commit()
        return jsonify({'message': 'Pembelian berhasil dihapus'})
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus pembelian', 'error': str(e)})
