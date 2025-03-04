import json
import os
from flask import Flask, Blueprint
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from mongoengine import connect
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

connect(host=os.getenv("MONGODB_URI"), name="db")

from api_server.api import api_bp
from api_server.utils import RANResourceConverter

app.url_map.converters["ran_resource"] = RANResourceConverter

app.register_blueprint(api_bp)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = 'application/json'
    return response
