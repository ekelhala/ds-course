from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound

from api_server.models import RANResource

class RANResourceConverter(BaseConverter):
    
    def to_python(self, value):
        #pylint: disable=no-member
        db_resource = RANResource.objects(resource_id=value)
        if db_resource is None:
            raise NotFound(f"Resource with id {value} does not exist")
        return db_resource.resource_id

    def to_url(self, value):
        return value.resource_id
