from composr.models.service import Service
from composr.models.service_attributes import PortMapping

class ComposeProject:
    def __init__(self, filename, name = None):
        self.data = {
            **({"name": name} if name else {}),
            "services": [
                Service(
                    "nginx:latest",
                    "nginx",
                    [PortMapping(8080, 8080, None, PortMapping.Protocol.TCP)],
                )
            ],
        }
        self.filename = filename

    def get_name(self):
        return self.data["name"]

    def get_filename(self):
        return self.filename