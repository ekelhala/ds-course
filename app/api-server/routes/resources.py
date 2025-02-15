from typing import List
from fastapi import APIRouter

from routes.schemas import ResourceRequest, ResourceCreationResponse, Resource

router = APIRouter()

@router.post("/", response_model=ResourceCreationResponse)
def request_resources(req: ResourceRequest):
    """
    Request for provisioning of resources (CU, DU)
    sends connection details for the core-CU connection as a
    response if successfull
    """

@router.get("/", response_model=List[Resource])
def get_resources():
    """
    Returns the resources currently in use by the client
    and the connection details for those resources.
    """
