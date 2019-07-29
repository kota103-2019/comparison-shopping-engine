from flask import render_template, url_for, request, session, redirect
from comparison import app
from comparison.models import *

pencarian = MainPencarian()

kategori_object = Kategori()
kategori_data = kategori_object.getKategori()

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "

    return render_template('home.html', kategori_list = kategori_data, kataKunci = "") 


@app.route("/search", methods = ['GET','POST'])
def search():
    if request.method == 'GET':
        # pencarianProduk(keyword=request.args.get('query'))
        pencarian.kataKunci = request.args.get('query')
        pencarian.hargaMin = 0.0
        pencarian.hargaMax = 0.0
        min_value = request.args.get('minimum')
        if min_value:
            pencarian.hargaMin = float(min_value)
        max_value = request.args.get('maximum')
        if max_value:
            pencarian.hargaMax = float(max_value)
        sort_by = request.args.get('sort')
        if sort_by:
            pencarian.jenisSort = sort_by
        sort_type = request.args.get('type')
        if sort_type:
            pencarian.caraSort = sort_type
        page = request.args.get('page')
        if not page or int(page)<1:
            page = 1
        listOfProduk, jmlprod = pencarian.mencariProdukByKataKunciRanked(page_num=page)
        infoHarga = InformasiHarga()
        infoHarga.listOfProduk = listOfProduk
        infoHarga.setInfoHarga()
        current_path = request.path + "?query=" + pencarian.kataKunci
        return render_template(
            'search.html', 
            kategori_list = kategori_data, 
            jmlprod = jmlprod, 
            listKota = pencarian.listKota, 
            kataKunci = pencarian.kataKunci,
            listOfProduk = listOfProduk, 
            infoHarga = infoHarga, 
            byKategori = False, 
            current_path = current_path, 
            page=page
            )

@app.route("/category/<idkat>")
def searchCateg(idkat):
    # pencarianProduk(idkat=idkat)
    pencarian.idKategori = idkat
    parent = request.args.get('parent')
    pencarian.hargaMin = 0.0
    pencarian.hargaMax = 0.0
    min_value = request.args.get('minimum')
    if min_value:
        pencarian.hargaMin = float(min_value)
    max_value = request.args.get('maximum')
    if max_value:
        pencarian.hargaMax = float(max_value)
    sort_by = request.args.get('sort')
    if sort_by:
        pencarian.jenisSort = sort_by
    sort_type = request.args.get('type')
    if sort_type:
        pencarian.caraSort = sort_type
    page = request.args.get('page')
    if not page or int(page)<1:
        page = 1
    listOfProduk, jmlprod = pencarian.mencariProdukByKategori(parent, page)
    infoHarga = InformasiHarga()
    infoHarga.listOfProduk = listOfProduk
    infoHarga.setInfoHarga()
    current_path = request.path + "?source=from_navbar"
    kataKunci = kategori_object.getKategoriDetail(idkat)
    return render_template(
        'search.html', 
        kategori_list = kategori_data, 
        jmlprod = jmlprod, 
        listKota = pencarian.listKota, 
        kataKunci = kataKunci['namakategori'], 
        listOfProduk = listOfProduk, 
        infoHarga = infoHarga, 
        byKategori = True,
        current_path = current_path, 
        page=page
        )

@app.route("/compare")
def compare():
    if request.method == 'POST':
        listIdProduk = request.form.getlist('checkproduct')
        err_msg = "Hasil Perbandingan"
        
        if len(listIdProduk)>4:
            err_msg = "Produk yang dipilih lebih dari 4"
            listOfProduk = []
            infoHarga = ""
        else:
            listOfProduk = pencarian.compare(listIdProduk)
            infoHarga = InformasiHarga()
            infoHarga.listOfProduk = listOfProduk
            infoHarga.setInfoHarga()

        return render_template(
            'compare.html', 
            error=err_msg, 
            listOfProduk = listOfProduk,            
            infoHarga = infoHarga,
            kategori_list = kategori_data, 
            )

# @app.route("/product-detail/<id>")
@app.route("/product", methods = ['GET','POST'])
def product_detail():
    if request.method == 'GET':
        idP = request.args.get('id')
        produk = Produk()
        produk.lihatDetailProduk(idP)
        return render_template(
            'detail.html', 
            kategori_list = kategori_data, 
            produk = produk
            )

# def detail(id):
#     return render_template('product-detail.html')
