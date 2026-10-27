from composr.models.service import Service
from composr.models.service_attributes import PortMapping, VolumeMapping, EnvFile, DependsOn
from composr.util.yaml_convertion import write_yaml

class ComposeProject:
    def __init__(self, filename, name = None):
        self.filename = filename
        self.name = None
        self.services = [
            Service(
                "nginx:latest",
                "nginx",
                [
                    PortMapping(8080, 8080, None, PortMapping.Protocol.TCP),
                    PortMapping(8090, 1234, "127.0.0.1", PortMapping.Protocol.UDP),
                    PortMapping(9067, 80, None, None)
                ],
                [
                    VolumeMapping("/mnt/storage/test", "/data/test", VolumeMapping.AccessMode.READ_ONLY),
                ],
                [
                    EnvFile("/mnt/storage/.env"),
                    EnvFile("/mnt/other/.env"),
                ],
                [
                    DependsOn("db", DependsOn.Condition.COMPLETED, True)
                ]
            ),
            Service(
                "postgres:16",
                "db",
                [
                    PortMapping(5432, 5432, "127.0.0.1", PortMapping.Protocol.TCP),
                ],
                [
                    VolumeMapping("/mnt/storage/postgres", "/var/lib/postgresql/data", None),
                ],
                [
                    EnvFile("/mnt/storage/db.env"),
                ],
            ),
            Service(
                "redis:7",
                "cache",
                [
                    PortMapping(6379, 6379, None, PortMapping.Protocol.TCP),
                ],
                None,
                None,
                [
                    DependsOn("db", DependsOn.Condition.HEALTHY, False),
                ],
            ),
        ]

    def get_name(self):
        return self.name

    def get_filename(self):
        return self.filename

    def write(self):
        write_yaml(self.to_dict(), self.filename)

    def to_dict(self) -> dict:
        return {
            **({"name": self.name} if self.name else {}),
            "services": {svc.name: svc.to_dict() for svc in self.services},
        }