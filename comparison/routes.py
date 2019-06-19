from flask import render_template, url_for, request, session, redirect
from comparison import app
#from comparison.models import

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "
    jmlprod = 9
    return render_template('home.html', jmlprod = jmlprod)

@app.route("/search", methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        kataKunci = request.form['searchbox']
    return render_template('search.html',kataKunci = kataKunci)

@app.route("/categ")
def searchCateg():
    return render_template('category.html')

@app.route("/compare")
def compare():
    return render_template('category.html')

# @app.route("/product-detail/<id>")
@app.route("/product_detail", methods = ['GET','POST'])
def product_detail():
    if request.method == 'POST':
        return render_template('product_detail.html')
# def detail(id):
#     return render_template('product-detail.html')
