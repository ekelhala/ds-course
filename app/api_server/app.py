from flask import Flask, Blueprint
from flask_restful import Api

from api_server.resources.RANResources import RANResourceCollection

app = Flask(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")
app.register_blueprint(api_bp)

api = Api(app)

api.add_resource(RANResourceCollection, "/ran_resources/")
