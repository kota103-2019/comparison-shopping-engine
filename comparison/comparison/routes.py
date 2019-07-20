from flask import render_template, url_for, request, session, redirect, jsonify
from comparison import app
from comparison.models import *

pencarian = MainPencarian()

kategori_object = Kategori()
kategori_data = kategori_object.getKategori()

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "
    return render_template('home.html', kategori_list = kategori_data) 

@app.route("/search", methods = ['GET','POST'])
def search():
    if request.method == 'GET':
        pencarian.kataKunci = request.args.get('query')
        pencarian.hargaMin = 0.0
        pencarian.hargaMax = 0.0
        if request.args.get('minimum'):
            pencarian.hargaMin = float(request.args.get('minimum'))
        if request.args.get('maximum'):
            pencarian.hargaMax = float(request.args.get('maximum'))
        listOfProduk = pencarian.mencariProdukByKataKunci()
        jmlprod = len(listOfProduk)
        infoHarga = InformasiHarga()
        infoHarga.setInfoHarga(listOfProduk)
        return render_template('search.html', kategori_list = kategori_data, jmlprod = jmlprod, listKota = pencarian.listKota , kataKunci = pencarian.kataKunci, listOfProduk = listOfProduk , infoHarga = infoHarga)

@app.route("/categ")
def searchCateg():
    return render_template('category.html')

@app.route("/compare", methods = ['GET','POST'])
def compare():
    jml = 4
    if request.method == 'GET':
        return render_template('compare.html', jml=jml)

# @app.route("/product-detail/<id>")
@app.route("/product_detail", methods = ['GET','POST'])
def product_detail():
    if request.method == 'POST':
        idP = request.form['idProduk']
        produk = Produk()
        produk.lihatDetailProduk(idP)
        return render_template('detail.html', kategori_list = kategori_data, produk = produk)

# def detail(id):
#     return render_template('product-detail.html')
