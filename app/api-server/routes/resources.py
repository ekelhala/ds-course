import json
from typing import List
from fastapi import APIRouter, HTTPException

from routes.schemas import ResourceRequest, ResourceCreationResponse, Resource, CreationStatus
from amqp_client import AMQPClient

router = APIRouter()

amqp_client = AMQPClient()

@router.post("/", response_model=ResourceCreationResponse)
def request_resources(req: ResourceRequest):
    """
    Request for provisioning of resources (CU, DU)
    sends connection details for the core-CU connection as a
    response if successful
    """
    try:
        amqp_client.connect()
        amqp_client.send(json.dumps({
            "core_ip": req.core_ip,
            "core_port": req.core_port,
            "num_rus": req.num_rus
        }))
        amqp_client.close()
        return {
            "resource": {
                "bind_address":"",
                "num_rus": 1
            },
            "status": CreationStatus.OK,
            "message": "test"
        }
    except KeyError as e:
        raise HTTPException(400, "Missing fields") from e

@router.get("/", response_model=List[Resource])
def get_resources():
    """
    Returns the resources currently in use by the client
    and the connection details for those resources.
    """
