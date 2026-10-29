from dataclasses import dataclass
from enum import Enum
from typing import Any
from composr.util.formatter import format_port

@dataclass(repr=False, eq=False)
class PortMapping:
    """
    The ports are used to define the port mappings between the host machine and the containers. This is crucial for allowing external access to services running inside containers.
    \nThis class uses the short syntax.
    \n\nhttps://docs.docker.com/reference/compose-file/services/#ports
    """

    class Protocol(Enum):
        TCP = "tcp"
        UDP = "udp"

    host_port: int | tuple[int, int]
    container_port: int | tuple[int, int]
    host_ip: str | None
    protocol: Protocol | None

    def __str__(self):
        return f"{self.host_ip + ':' if self.host_ip is not None else ''}{format_port(self.host_port)}:{format_port(self.container_port)}{'/' + self.protocol.value if self.protocol is not None else ''}"

@dataclass(repr=False, eq=False)
class VolumeMapping:
    """
    The volumes attribute define mount host paths or named volumes that are accessible by service containers.
    \nThis class uses the short syntax.
    \n\nhttps://docs.docker.com/reference/compose-file/services/#volumes
    """

    class AccessMode(Enum):
        READ_WRITE = "rw"
        READ_ONLY = "ro"

    host_volume: str
    container_path: str
    access_mode: AccessMode | None

    def __str__(self):
        return f"{self.host_volume}:{self.container_path}{':' + self.access_mode.value if self.access_mode is not None else ''}"

@dataclass(repr=False, eq=False)
class EnvFile:
    """
    The env_file attribute is used to specify one or more files that contain environment variables to be passed to the containers.
    This class does not support the long syntax (yet) and therefore doesn't have the "required" attribute
    \n\nhttps://docs.docker.com/reference/compose-file/services/#env_file
    """

    path: str

    def __str__(self):
        return self.path

@dataclass(repr=False, eq=False)
class DependsOn:
    """
    With the depends_on attribute, you can control the order of service startup and shutdown. It is useful if services are closely coupled, and the startup sequence impacts the application's functionality.
    \nThis class supports the short and the long syntax, depending on the given data.
    \n\nhttps://docs.docker.com/reference/compose-file/services/#depends_on
    """

    class Condition(Enum):
        STARTED = "service_started"
        HEALTHY = "service_healthy"
        COMPLETED = "service_completed_successfully"

    container_name: str
    condition: Condition
    restart: bool

    def to_dict(self):
        result: dict[str, Any] = {"condition": self.condition.value}

        if self.restart is not None:
            result["restart"] = self.restart

        return result
