import importlib.metadata
import yaml

from composr.models.service_attributes import PortMapping, VolumeMapping, EnvFile

HEADER = f"# Generated with Composr v{importlib.metadata.version("composr")}: https://github.com/mxiwbr/composr\n"

class _ComposeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def _str_representer(dumper, obj):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(obj))

def _quoted_str_representer(dumper, obj):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(obj), style='"')

def to_yaml(data: dict) -> str:
    return HEADER + yaml.dump(data, Dumper=_ComposeDumper, sort_keys=False)

def write_yaml(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_yaml(data))

_ComposeDumper.add_multi_representer(PortMapping, _quoted_str_representer)
_ComposeDumper.add_multi_representer(VolumeMapping, _str_representer)
_ComposeDumper.add_multi_representer(EnvFile, _str_representer)