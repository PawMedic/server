from . import api
from .obat import Obat
from config import db
from flask import jsonify, request

@api.route('/obat', methods=['GET'])
def get_obat():
    obat = db.session.query(Obat).all()
    if obat:
        data = [o.json() for o in obat]
        return jsonify(data)
    else:
        return jsonify({'message': 'Tidak ada obat'})

@api.route('/obat/<id>', methods=['GET'])
def get_obat_by_id(id):
    obat = db.session.query(Obat).filter_by(id=id).first()
    if obat:
        return jsonify(obat.json())
    else:
        return jsonify({'message': 'Obat tidak ditemukan'})

@api.route('/obat', methods=['POST'])
def add_obat():
    nama = request.json['nama']
    jenis = request.json['jenis']
    harga_jual = request.json['harga_jual']
    harga_beli = request.json['harga_beli']
    kategori = request.json['kategori']
    stock = request.json['stock']

    try:
        obat = Obat(nama=nama, jenis=jenis, harga_jual=harga_jual, harga_beli=harga_beli, kategori=kategori, stock=stock)
        db.session.add(obat)
        db.session.commit()
        return jsonify({'message': 'Obat berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'message': 'Gagal menambahkan obat', 'error': str(e)})

@api.route('/obat/<id>', methods=['PUT'])
def update_obat(id):
    obat = db.session.query(Obat).filter_by(id=id).first()
    if not obat:
        return jsonify({'message': 'Obat tidak ditemukan'})

    obat.nama = request.json.get('nama', obat.nama)
    obat.jenis = request.json.get('jenis', obat.jenis)
    obat.harga_jual = request.json.get('harga_jual', obat.harga_jual)
    obat.harga_beli = request.json.get('harga_beli', obat.harga_beli)
    obat.kategori = request.json.get('kategori', obat.kategori)
    obat.stock = request.json.get('stock', obat.stock)

    try:
        db.session.commit()
        return jsonify({'message': 'Obat berhasil diperbarui'})
    except Exception as e:
        return jsonify({'message': 'Gagal memperbarui obat', 'error': str(e)})

@api.route('/obat/<id>', methods=['DELETE'])
def delete_obat(id):
    obat = db.session.query(Obat).filter_by(id=id).first()
    if not obat:
        return jsonify({'message': 'Obat tidak ditemukan'})

    try:
        db.session.delete(obat)
        db.session.commit()
        return jsonify({'message': 'Obat berhasil dihapus'})
    except Exception as e:
        return jsonify({'message': 'Gagal menghapus obat', 'error': str(e)})
