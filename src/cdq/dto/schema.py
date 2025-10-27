from typing import Optional, Type, Iterator

import pyarrow as pa
from pydantic import BaseModel, Field, PrivateAttr



def _as_arrow(type_: Type) -> pa.DataType:
    if type_ is str:
        return pa.string()
    if type_ is float:
        return pa.float64()
    if type_ is int:
        return pa.int64()
    raise TypeError(f"unsupported type provided {type_}")


class FieldModel(BaseModel):
    name: str
    type: Type

    @property
    def type_arrow(self) -> pa.DataType:
        return _as_arrow(self.type)

class FieldContainer(BaseModel):
    _fields: dict[str, FieldModel] = PrivateAttr(default_factory=dict)

    def add(self, field: FieldModel):
        self._fields[field.name] = field

    def __iter__(self) -> Iterator[FieldModel]:
        return iter(self._fields.values())

    def get(self, item):
        return self._fields[item]


class Schema(BaseModel):
    typemap: Optional[dict] = None
    fields: FieldContainer = Field(default_factory=FieldContainer)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.typemap:  # post-init analog
            self.typemap = self.typemap_define()
        self.fields = FieldContainer()
        for k, v in self.typemap.items():
            field = FieldModel(name=k, type=v)
            self.fields.add(field)

    def typemap_define(self) -> dict:
        raise NotImplementedError

    def project(self) -> dict:
        raise NotImplementedError

    def to_dict(self):
        return self.project()

    def as_arrow(self) -> pa.Schema:
        mapping = {field.name: field.type_arrow for field in self.fields}
        return pa.schema(mapping)