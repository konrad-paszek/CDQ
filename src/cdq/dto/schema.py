from dataclasses import dataclass
from typing import Optional, Type

import pyarrow as pa

from .base import Dto


def _as_arrow(type_):
    if type_ is str:
        return pa.string()
    if type_ is float:
        return pa.float64()
    if type_ is int:
        return pa.int64()
    # TODO: any idea how we could map categorical types?
    return TypeError(f"unsupported type provided {type_}")


@dataclass
class Field:
    name: str
    type: Type

    @property
    def type_arrow(self):
        return _as_arrow(self.type)


class FieldContainer:
    def __iter__(self):
        pass


@dataclass
class Schema(Dto):
    typemap: Optional[dict] = None

    def __post_init__(self):
        self.fields = FieldContainer()
        if not self.typemap:
            self.typemap = self.typemap_define()
        for k, v in self.typemap.items():
            field = Field(k, v)
            setattr(self.fields, k, field)

    def typemap_define(self) -> dict:
        raise NotImplementedError

    def project(self) -> dict:
        raise NotImplementedError

    def to_dict(self):
        return self.project()

    def as_arrow(self) -> pa.Schema:
        mapping = {}
        # TODO: why not using field container iterator protocol?
        for v in self.fields.__dict__.values():
            if isinstance(v, Field):
                mapping.update({v.name: v.type_arrow})
        return pa.schema(mapping)
