from . import api
from .penjualan import Penjualan
from config import db
from flask import jsonify, request

@api.route('/penjualan', methods=['GET'])
def get_penjualan():
    penjualan = db.session.query(Penjualan).all()
    if penjualan:
        data = [p.json() for p in penjualan]
        return jsonify(data)
    else:
        return jsonify({'message': 'Tidak ada data penjualan'})

@api.route('/penjualan/<kode>', methods=['GET'])
def get_penjualan_by_kode(kode):
    penjualan = db.session.query(Penjualan).filter_by(kode=kode).first()
    if penjualan:
        return jsonify(penjualan.json())
    else:
        return jsonify({'message': 'Penjualan tidak ditemukan'})

@api.route('/penjualan', methods=['POST'])
def add_penjualan():
    kode = request.json['kode']
    jenis = request.json['jenis']

    try:
        penjualan = Penjualan(kode=kode, jenis=jenis)
        db.session.add(penjualan)
        db.session.commit()
        return jsonify({'message': 'Penjualan berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan penjualan', 'error': str(e)})

@api.route('/penjualan/<kode>', methods=['PUT'])
def update_penjualan(kode):
    penjualan = db.session.query(Penjualan).filter_by(kode=kode).first()
    if not penjualan:
        return jsonify({'message': 'Penjualan tidak ditemukan'})

    penjualan.jenis = request.json.get('jenis', penjualan.jenis)

    try:
        db.session.commit()
        return jsonify({'message': 'Penjualan berhasil diperbarui'})
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui penjualan', 'error': str(e)})

@api.route('/penjualan/<kode>', methods=['DELETE'])
def delete_penjualan(kode):
    penjualan = db.session.query(Penjualan).filter_by(kode=kode).first()
    if not penjualan:
        return jsonify({'message': 'Penjualan tidak ditemukan'})

    try:
        db.session.delete(penjualan)
        db.session.commit()
        return jsonify({'message': 'Penjualan berhasil dihapus'})
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus penjualan', 'error': str(e)})
