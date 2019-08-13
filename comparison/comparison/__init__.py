from flask import Flask
import json
import datetime
from bson.objectid import ObjectId
from .extensions import mongo
# import settings

#from comparison.extensions import mongo

#def create_app(config_object ='settings' ):
app = Flask(__name__)
# config_object = 'comparison.settings'
# app.config.from_object(config_object)
#app.config["MONGO_URI"] = "mongodb+srv://faiz:bismillah@cluster0-sr9cz.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/comparison-shopping-engine"
#app.json_encoder = JSONEncoder
# mongo = PyMongo(app)
mongo.init_app(app)
from comparison import routes

   #return app

from comparison import routes