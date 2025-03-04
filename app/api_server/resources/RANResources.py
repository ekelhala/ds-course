import json
from flask import request, Response
from flask_restful import Resource
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError, BadRequest
from jsonschema import validate, ValidationError

from api_server.amqp_client import AMQPClient
from api_server.models import RANResource

amqp_client = AMQPClient()

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

    def delete(self, ran_resource):
        request_body = {
            "command": "delete",
            "data": {"resource_id": ran_resource.resource_id}
        }
        amqp_client.connect()
        worker_response = amqp_client.send(request_body)
        if worker_response["status"] == "ok":
            ran_resource.delete()
            return "Resource deleted"
        raise InternalServerError(
                                "An error occured when deleting the RAN resource",
                                worker_response["data"]["message"])


class RANResourceCollection(Resource):

    def post(self):
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        try:
            validate(request.json, RANResourceItem.json_schema())
        except ValidationError as e:
            raise BadRequest(str(e.message)) from e
        amqp_client.connect()
        worker_response = amqp_client.send(json.dumps({
            "command": "create",
            "data": {
                "core_ip": request.json["core_ip"],
                "core_port": request.json["core_port"],
                "num_rus": request.json["num_rus"]
            }
        }))
        amqp_client.close()
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
        raise InternalServerError("Could not create RAN resource")
