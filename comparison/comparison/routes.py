from flask import render_template, url_for, request, session, redirect, jsonify
from comparison import app

from comparison.models import *

pencarian = MainPencarian()

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "
    return render_template('home.html')

@app.route("/search", methods = ['GET','POST'])
def search():
        #pencarian = MainPencarian()
        if request.method == 'POST':
                pencarian.kataKunci = request.form['searchbox']
                listOfProduk = pencarian.mencariProdukByKataKunci()
                jmlprod = len(listOfProduk)
                infoHarga = InformasiHarga()
                infoHarga.setInfoHarga(listOfProduk)
                return render_template('search.html', jmlprod = jmlprod, kataKunci = pencarian.kataKunci, listOfProduk = listOfProduk, infoHarga = infoHarga)
        if request.method == 'GET':
                pencarian.hargaMin = 0.0
                pencarian.hargaMax = 0.0
                if request.args.get('minprice'):
                        pencarian.hargaMin = float(request.args.get('minprice'))
                if request.args.get('maxprice'):
                        pencarian.hargaMax = float(request.args.get('maxprice'))
                listOfProduk = pencarian.mencariProdukByKataKunci()
                jmlprod = len(listOfProduk)
                infoHarga = InformasiHarga()
                infoHarga.setInfoHarga(listOfProduk)
                return render_template('search.html', jmlprod = jmlprod, kataKunci = pencarian.kataKunci, listOfProduk = listOfProduk , infoHarga = infoHarga)

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
            return render_template('product_detail.html',produk = produk)

# def detail(id):
#     return render_template('product-detail.html')
