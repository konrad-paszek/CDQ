import os
import tempfile
from pathlib import Path
from typing import List
from pydantic import BaseModel, PrivateAttr
import pyarrow.fs as fs

from cdq.dto.fileinfo import FileInfo

class ResultContext(BaseModel):
    basedir: os.PathLike
    _fs: fs.FileSystem = PrivateAttr()
    _prefix: str = PrivateAttr()
    _dir: Path = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._prefix = tempfile.mkdtemp()
        self._fs = fs.LocalFileSystem()
        self._dir = Path(f"{self._prefix}/{self.basedir}/")
        self._fs.create_dir(self._dir.as_posix())

    def to_dict(self):
        return {"workdir": self.workdir.as_posix(), "content": self.inspect()}

    @property
    def filesystem(self) -> fs.FileSystem:
        return self._fs

    @property
    def workdir(self) -> Path:
        return self._dir

    def teardown(self):
        import shutil
        shutil.rmtree(self.workdir, ignore_errors=False)

    def inspect(self) -> List[FileInfo]:
        infos = self.filesystem.get_file_info(
            fs.FileSelector(self.workdir.as_posix(), recursive=True)
        )
        return [FileInfo(path=info.path) for info in infos]
# NOTE: what about other file systems (e.g. S3)?

class HandledResponse(BaseModel):
    status: str
    context: ResultContext

    def to_dict(self):
        return {"status": self.status, "context": self.context.to_dict()}

    def set_running(self):
        self.status = "RUNNING"

    def set_finished(self):
        self.status = "FINISHED"

    def set_error(self):
        self.status = "ERROR"
