from flask import Flask

#from comparison.extensions import mongo

#def create_app(config_object ='settings' ):
app = Flask(__name__)
#app.config.from_object(config_object)
#app.config
#mongo.init_app(app)
from comparison import routes

   #return app