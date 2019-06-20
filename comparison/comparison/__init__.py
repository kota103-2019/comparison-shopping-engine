from flask import Flask
import json
import datetime
from bson.objectid import ObjectId
from .extensions import mongo

#class JSONEncoder(json.JSONEncoder):
#    ''' extend json-encoder class'''

#    def default(self, o):
 #       if isinstance(o, ObjectId):
  #          return str(o)
   #     if isinstance(o, datetime.datetime):
    #        return str(o)
     #   return json.JSONEncoder.default(self, o)

app = Flask(__name__)
#config_object = 'comparison.settings'
#app.config.from_object(config_object)
#app.config["MONGO_URI"] = "mongodb+srv://faiz:bismillah@cluster0-sr9cz.mongodb.net/test?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://localhost:27017/comparison"
#app.json_encoder = JSONEncoder
mongo.init_app(app)

from comparison import routes