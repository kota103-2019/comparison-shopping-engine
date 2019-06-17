from flask import render_template, url_for, request, session, redirect
from comparison import app
#from comparison.models import

@app.route("/")
def index():
    #kota = mongo.db.kota.find({"idProv": 11})
    #str = "hello "
    return render_template('home.html')

@app.route("/search/<keyword>")
def search(keyword):
    #str = "hello "+keyword
    return render_template('search.html')

@app.route("/categ")
def searchCateg():
    return render_template('category.html')

@app.route("/compare")
def compare():
    return render_template('category.html')

# @app.route("/product-detail/<id>")
@app.route("/product_detail", methods = ['GET','POST'])
def product_detail():
    Pokemons =["Pikachu", "Charizard", "Squirtle", "Jigglypuff",
           "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]
    if request.method == 'POST':
        return render_template('product_detail.html',len=5, Pokemons = Pokemons)
# def detail(id):
#     return render_template('product-detail.html')
