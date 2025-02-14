from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def request_resources():
    """
    Request for provisioning of resources (CU, DU)
    sends connection details for the core-CU connection as a
    response if successfull
    """

@router.get("/")
def get_resources():
    """
    Returns the resources currently in use by the client
    and the connection details for those resources.
    """
