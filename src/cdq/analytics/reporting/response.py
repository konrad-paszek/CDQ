import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pyarrow.fs as fs


@dataclass
class ResultContext:
    basedir: os.PathLike
    _fs: fs.FileSystem = field(init=False)
    _prefix: str = field(init=False)
    _dir: Path = field(init=False)

    def to_dict(self):
        return {"workdir": self.workdir.as_posix(), "content": self.inspect()}

    def __post_init__(self):
        self._prefix = tempfile.mkdtemp()
        self._fs = fs.LocalFileSystem()
        self._dir = Path(f"{self._prefix}/{self.basedir}/")
        self._fs.create_dir(self._dir.as_posix())

    @property
    def filesystem(self) -> fs.FileSystem:
        return self._fs

    @property
    def workdir(self) -> Path:
        return self._dir

    def teardown(self):
        import shutil
        shutil.rmtree(self.workdir, ignore_errors=False)

    def inspect(self):
        # NOTE: why not wrapping these with cdq.dto.FileInfo?
        return self.filesystem.get_file_info(
            fs.FileSelector(self.workdir.as_posix(), recursive=True)
        )
# NOTE: what about other file systems (e.g. S3)?

@dataclass
class HandledResponse:
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
