from typing import Any

from composr.models.service_attributes import PortMapping, VolumeMapping, EnvFile, DependsOn

class Service:

    image: str
    name: str
    ports: list[PortMapping] | None
    volumes: list[VolumeMapping] | None
    env_file: list[EnvFile] | None
    depends_on: list[DependsOn] | None

    def __init__(
            self,
            image: str,
            name: str,
            ports: list[PortMapping] | None = None,
            volumes: list[VolumeMapping] | None = None,
            env_file: list[EnvFile] | None = None,
            depends_on: list[DependsOn] | None = None
    ):
        self.image = image
        self.name = name
        self.ports = ports
        self.volumes = volumes
        self.env_file = env_file
        self.depends_on = depends_on

    def to_dict(self) -> dict:

        fields = {
            "image": self.image,
            "ports": self.ports,
            "volumes": self.volumes,
            "env_file": self.env_file,
            "depends_on": self.depends_on
        }

        result: dict[str, Any] = {key: value for key, value in fields.items() if value}

        if self.depends_on:
            result["depends_on"] = {dep.container_name: dep.to_dict() for dep in self.depends_on}

        return result