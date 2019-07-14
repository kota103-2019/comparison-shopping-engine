from flask import render_template, url_for, request, session, redirect
from comparison import app
#from comparison.models import

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
                return render_template('search.html', jmlprod = jmlprod, listKota =pencarian.listKota , kataKunci = pencarian.kataKunci, listOfProduk = listOfProduk , infoHarga = infoHarga)

@app.route("/categ")
def searchCateg():
    return render_template('category.html')

@app.route("/compare")
def compare():
    return render_template('category.html')

# @app.route("/product-detail/<id>")
@app.route("/product-detail", methods = ['POST','GET'])
def productdetail():
    if request.method == 'POST':
        productdetail = request.form
        return render_template('product-detail.html', productdetail = productdetail)
# def detail(id):
#     return render_template('product-detail.html')
