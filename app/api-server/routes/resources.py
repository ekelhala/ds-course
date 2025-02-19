from typing import List
from fastapi import APIRouter, HTTPException

from routes.schemas import ResourceRequest, ResourceCreationResponse, Resource, CreationStatus
from amqp_client import AMQPClient

router = APIRouter()

amqp_client = AMQPClient()
amqp_client.connect()

@router.post("/", response_model=ResourceCreationResponse)
def request_resources(req: ResourceRequest):
    """
    Request for provisioning of resources (CU, DU)
    sends connection details for the core-CU connection as a
    response if successful
    """
    try:
        amqp_client.send({
            "core_ip": req.core_ip,
            "core_port": req.core_port,
            "num_rus": req.num_rus
        })
        return {
            "resource": None,
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
