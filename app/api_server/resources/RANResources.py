import json
from flask import request, Response
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError

from api_server.amqp_client import AMQPClient
from api_server.models import RANResource

class RANResourceItem(Resource):

    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "required": ["core_ip", "core_port", "num_rus"],
            "properties": {
                "core_ip": {"type": "string"},
                "core_port": {"type": "number"},
                "num_rus": {"type": "number"}
            }
        }

class RANResourceCollection(Resource):

    def __init__(self):
        self.amqp_client = AMQPClient()

    def post(self):
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        self.amqp_client.connect()
        worker_response = self.amqp_client.send(json.dumps({
            "command": "create",
            "data": {
                "core_ip": request.json["core_ip"],
                "core_port": request.json["core_port"],
                "num_rus": request.json["num_rus"]
            }
        }))
        self.amqp_client.close()
        if worker_response["status"] == "ok":
            ran_resource = RANResource(
                core_ip=request.json["core_ip"],
                core_port=request.json["core_port"],
                num_rus=request.json["num_rus"],
                resource_id=worker_response["data"]["id"]
            )
            ran_resource.save()
            return Response(
                ran_resource.to_json(),
                201,
                mimetype="application/json"
            )
        raise InternalServerError("Could not create resource")
