from mongoengine import Document, StringField, IntField


class RANResource(Document):
    resource_id = StringField()
    core_ip = StringField()
    core_port = IntField()
    num_rus = IntField()

    meta = {
        "collection": "ranresources"
    }

    def to_json(self):
        return {
            "resource_id": self.resource_id,
            "core_ip": self.core_ip,
            "core_port": self.core_port,
            "num_rus": self.num_rus
        }
