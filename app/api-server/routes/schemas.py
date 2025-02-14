from pydantic import BaseModel

class ResourceRequest(BaseModel):
    """
    A schema representing the data needed for
    provisioning new resources
    """
    num_rus: int # number of RUs to connect to
    core_ip: str # AMF IP address of the core network for CU
    core_port: int # AMF port of the core for CU to connect to
