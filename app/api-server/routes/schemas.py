from enum import Enum
from pydantic import BaseModel

class ResourceRequest(BaseModel):
    """
    A schema representing the data needed for
    provisioning new resources
    """
    num_rus: int # number of RUs to connect to
    core_ip: str # AMF IP address of the core network for CU
    core_port: int # AMF port of the core for CU to connect to

class ResponseStatus(Enum):
    OK = "ok"
    ERROR = "error"
    ERROR_NOT_ENOUGH_RESOURCES = "error_not_enough_resources"

class Resource(BaseModel):
    """
    Schema representing a single resource
    """
    bind_address: str = None # IP address where the CU is listening for connections
    num_rus: int = None # number of connected RUs

class ResourceCreationResponse(BaseModel):
    """
    A schema representing the allocated resources
    and connection details
    """
    resource: Resource
    status: ResponseStatus # indicates the result of the request
    message: str = "" # message that provides more information
    resource_id: str = "" # unique id for the resource
