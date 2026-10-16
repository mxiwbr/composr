from composr.models.service_attributes import PortMapping, VolumeMapping, EnvFile, DependsOn

class Service:

    image: str
    container_name: str | None
    ports: list[PortMapping] | None
    volumes: list[VolumeMapping] | None
    env_file: list[EnvFile] | None
    depends_on: list[DependsOn] | None

    def __init__(
            self,
            image: str,
            container_name: str | None = None,
            ports: list[PortMapping] | None = None,
            volumes: list[VolumeMapping] | None = None,
            env_file: list[EnvFile] | None = None,
            depends_on: list[DependsOn] | None = None
    ):
        self.image = image
        self.container_name = container_name
        self.ports = ports
        self.volumes = volumes
        self.env_file = env_file
        self.depends_on = depends_on
