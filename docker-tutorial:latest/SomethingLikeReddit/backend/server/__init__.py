from config import Config

from flask import Flask
api = Flask(__name__)

# load configuration module
api.config.from_object(Config)

from flask_cors import CORS
CORS(api)

# mongo connection
from flask_pymongo import PyMongo
mongo = PyMongo(api)
