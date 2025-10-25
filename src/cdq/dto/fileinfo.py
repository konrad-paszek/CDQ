import os
from dataclasses import dataclass


@dataclass
class FileInfo:
    path: os.PathLike

    @property
    def name(self):
        return os.path.basename(self.path)
