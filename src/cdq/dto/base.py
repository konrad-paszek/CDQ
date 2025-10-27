from pydantic import BaseModel


class Dto(BaseModel):
    def to_dict(self):
        return self.model_dump()
