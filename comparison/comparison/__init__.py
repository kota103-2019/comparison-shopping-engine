from flask import Flask
import json
import datetime
from bson.objectid import ObjectId
from .extensions import mongo
import settings

#from comparison.extensions import mongo

#def create_app(config_object ='settings' ):
app = Flask(__name__)
config_object = 'comparison.settings'
app.config.from_object(config_object)
#app.config["MONGO_URI"] = "mongodb+srv://faiz:bismillah@cluster0-sr9cz.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_URI"] = settingsp['MONGO_URI']
#app.json_encoder = JSONEncoder
mongo.init_app(app)

   #return app