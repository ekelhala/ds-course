import logging
import json
from typing import List
from fastapi import APIRouter, HTTPException

from routes.schemas import ResourceRequest, ResourceCreationResponse, Resource, ResponseStatus
from amqp_client import AMQPClient

router = APIRouter()

amqp_client = AMQPClient()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@router.post("/", response_model=ResourceCreationResponse)
def request_resources(req: ResourceRequest):
    """
    Request for provisioning of resources (CU, DU)
    sends connection details for the core-CU connection as a
    response if successful
    """
    try:
        amqp_client.connect()
        worker_response = amqp_client.send(json.dumps({
            "command": "create",
            "data": {
                "core_ip": req.core_ip,
                "core_port": req.core_port,
                "num_rus": req.num_rus
            }
        }))
        amqp_client.close()
        return {
            "resource": {
                "bind_address":"",
                "num_rus": 1
            },
            "status": ResponseStatus.OK,
            "message": worker_response["message"],
            "resource_id": worker_response["id"]
        }
    except KeyError as e:
        logging.error("error in POST: %s",str(e))
        raise HTTPException(400, "Missing fields") from e

@router.get("/", response_model=List[Resource])
def get_resources():
    """
    Returns the resources currently in use by the client
    and the connection details for those resources.
    """

@router.delete("/{resource_id}/")
def delete_resource(resource_id: str):
    """
    Deletes a resource (deployment) with given id
    """
    try:
        amqp_client.connect()
        worker_response = amqp_client.send(json.dumps({
            "command": "delete",
            "data": {
                "resource_id": resource_id
            }
        }))
        amqp_client.close()
        return {"status": ResponseStatus.OK, "message": worker_response["message"]}
    except:
        raise HTTPException(500, "Error deleting resource")
