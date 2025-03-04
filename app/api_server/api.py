from flask import Blueprint
from flask_restful import Api

from api_server.resources.RANResources import RANResourceCollection, RANResourceItem

api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp)

api.add_resource(RANResourceCollection, "/ran_resources/")
api.add_resource(RANResourceItem, "/ran_resources/<ran_resource:ran_resource>/")
