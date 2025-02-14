from pydantic import BaseModel

class ResourceRequest(BaseModel):
    """
    A schema representing the data needed for
    provisioning new resources
    """
    