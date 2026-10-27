from enum import Enum
from typing import Any


class PortMapping:
    """
    The ports are used to define the port mappings between the host machine and the containers. This is crucial for allowing external access to services running inside containers.
    \nThis class uses the short syntax.
    \n\nhttps://docs.docker.com/reference/compose-file/services/#ports
    """

    class Protocol(Enum):
        TCP = "tcp"
        UDP = "udp"

    host_ip: str | None
    host_port: int | tuple[int, int]
    container_port: int | tuple[int, int]
    protocol: Protocol | None

    def __init__(
            self,
            host_port: int | tuple[int, int],
            container_port: int | tuple[int, int],
            host_ip: str | None = None,
            protocol: Protocol | None = None
    ):
        self.host_ip = host_ip
        self.host_port = host_port
        self.container_port = container_port
        self.protocol = protocol

    def __str__(self):
        return f"{self.host_ip + ':' if self.host_ip is not None else ''}{self.format_port(self.host_port)}:{self.format_port(self.container_port)}{'/' + self.protocol.value if self.protocol is not None else ''}"

    def format_port(self, port) -> str:
        if isinstance(port, int):
            return str(port)
        elif isinstance(port, tuple):
            return f"{port[0]}-{port[1]}"
        else:
            return ""

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

    def __init__(
            self,
            host_volume: str,
            container_path: str,
            access_mode: AccessMode | None = None,
    ):
        self.host_volume = host_volume
        self.container_path = container_path
        self.access_mode = access_mode

    def __str__(self):
        return f"{self.host_volume}:{self.container_path}{':' + self.access_mode.value if self.access_mode is not None else ''}"

class EnvFile:
    """
    The env_file attribute is used to specify one or more files that contain environment variables to be passed to the containers.
    This class does not support the long syntax (yet) and therefore doesn't have the "required" attribute
    \n\nhttps://docs.docker.com/reference/compose-file/services/#env_file
    """

    path: str

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f"{self.path}"

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

    def __init__(
            self,
            container_name: str,
            condition: Condition = Condition.STARTED,
            restart: bool = False
    ):
        self.container_name = container_name
        self.condition = condition
        self.restart = restart

    def to_dict(self):
        result: dict[str, Any] = {"condition": self.condition.value}

        if self.restart is not None:
            result["restart"] = self.restart

        return result
