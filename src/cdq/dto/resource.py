from dataclasses import dataclass

from .base import Dto


@dataclass
class ResourceInfo(Dto):
    id: str
