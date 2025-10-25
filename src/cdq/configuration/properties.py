import abc
from typing import Any, Optional, Type

from .base import get_config

config = get_config()


class Property(abc.ABC):
    key: str

    def __init__(
        self,
        raises: bool = True,
        astype: Optional[Type] = None,
        default: Optional[Any] = None,
    ):
        self.default = default
        self.astype = astype
        self.raises = raises

    def __get__(self, instance, owner=None):
        return config.get(
            section_option=self.key,
            default=self.default,
            raises=self.raises,
            astype=self.astype,
        )


class MongoUrl(Property):
    key = "mongo.url"
