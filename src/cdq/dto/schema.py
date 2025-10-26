from dataclasses import dataclass, field
from typing import Optional, Type, Iterator

import pyarrow as pa

from .base import Dto


def _as_arrow(type_: Type) -> pa.DataType:
    if type_ is str:
        return pa.string()
    if type_ is float:
        return pa.float64()
    if type_ is int:
        return pa.int64()
    raise TypeError(f"unsupported type provided {type_}")


@dataclass
class Field:
    name: str
    type: Type

    @property
    def type_arrow(self) -> pa.DataType:
        return _as_arrow(self.type)

class FieldContainer:
    def __init__(self):
        self._fields = {}

    def add(self, field: Field):
        self._fields[field.name] = field

    def __iter__(self) -> Iterator[Field]:
        return iter(self._fields.values())

    def __getattr__(self, item):
        if item in self._fields:
            return self._fields[item]
        raise AttributeError(f"'FieldContainer' has no attribute '{item}'")


@dataclass
class Schema(Dto):
    typemap: Optional[dict] = field(default=None)

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
        mapping = {field.name: field.type_arrow for field in self.fields}
        return pa.schema(mapping)