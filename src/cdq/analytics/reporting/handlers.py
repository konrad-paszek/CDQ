import os
import zipfile

from cdq.data_processing import MongoParquetTransfer

from .response import HandledResponse, ResultContext


class Handler:
    @classmethod
    def handle(cls, request):
        raise NotImplementedError


class DefaultHandler(Handler):
    @classmethod
    def _zipfiles(cls, files, target, remove=True):
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file)
        for file in files:
            os.remove(file)

    @classmethod
    def handle(cls, request):
        # TODO: this function could use some refactoring
        schema = request.info.schema.cls()
        source = request.info.source.cls(storage=request.storage_id, schema=schema)

        ctx = ResultContext(basedir=request.context_path)
        resp = HandledResponse(status="UNKNOWN", context=ctx)
        transfer = MongoParquetTransfer(source=source, schema=schema, context=ctx)
        resp.set_running()
        # TODO: how to avoid hardcoding batch_size and name?
        dataset = transfer.to_dataset(batch_size=5, name="business_partners")
        ix = 1
        files = []
        for batch in dataset.to_batches(batch_size=10):
            report = request.info.report.cls(batch.to_pandas(), schema=schema)
            print("processing batch", ix)
            if request.format == "xlsx":
                filepath = ctx.workdir / f"{request.title}_{str(ix)}.xlsx"
                report.to_excel(filepath.as_posix())
                files.append(filepath)
            ix += 1
        zippath = ctx.workdir / f"{request.title}.zip"
        if files:
            print("preparing report archive")
            cls._zipfiles(files, target=zippath.as_posix())
        resp.set_finished()
        return resp
