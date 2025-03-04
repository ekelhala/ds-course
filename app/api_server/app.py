import os
from flask import Flask, Blueprint
from flask_restful import Api
from mongoengine import connect
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

connect(host=os.getenv("MONGODB_URI"), name="db")

from api_server.api import api_bp
from api_server.utils import RANResourceConverter

app.url_map.converters["ran_resource"] = RANResourceConverter

app.register_blueprint(api_bp)
