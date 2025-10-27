import os

from pydantic import BaseModel


class FileInfo(BaseModel):
    path: str

    @property
    def name(self):
        return os.path.basename(self.path)
