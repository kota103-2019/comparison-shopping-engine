from flask import render_template, url_for, request, session, redirect, jsonify
from comparison import app

from comparison.models import MainPencarian

pencarian = MainPencarian()

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "
    return render_template('home.html')

@app.route("/search", methods = ['GET','POST'])
def search():
    jmlprod = 9
    if request.method == 'POST':
        kataKunci = request.form['searchbox']
    return render_template('search.html', jmlprod = jmlprod, kataKunci = kataKunci)

@app.route("/search/<keyword>")
def search(keyword):
        pencarian.kataKunci = keyword
        listOfProduk = pencarian.mencariProdukByKataKunci()
        output = []
        for i in listOfProduk:
                output.append({'id':i['_id'],'Nama Produk':i['title'], 'Harga Awal':i['price_final'], 'img_url' : i['image_url']
                , 'Kondisi Barang' : i['condition'], 'Lokasi Toko' : i['seller_location'], 'Online Marketplace' : i['online_marketplace']
                , 'Nama Toko': i['seller'] , 'url' : i['url'] 
                })
        if len(output) < 1 :
                return 'Tidak ditemukan produk yang dimaksud'
        else:
                return jsonify({'List Produk':output})



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
        return render_template('product_detail.html')

# def detail(id):
#     return render_template('product-detail.html')
