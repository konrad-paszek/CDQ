import pyarrow as pa
import pyarrow.dataset as ds

from cdq.dto import Schema
from cdq.infra.mongodb import mongoclient


class DataSource:
    def read(self):
        raise NotImplementedError


class MongoDataSource(DataSource):
    def __init__(self, database, storage, schema):
        self.database = database
        self.storage = storage
        self.schema = schema
        self.match = {}
        self.projection = self.schema.project()

    def read(self):
        with mongoclient() as mongo:
            db = mongo.get_database(self.database)
            collection = db.get_collection(self.storage)
            # NOTE: works for simple pipelines, but what
            # if we'd require an unwind stage?
            pipeline = []
            if self.match:
                pipeline.insert(0, {"$match": self.match})
            if self.projection:
                pipeline.append({"$project": self.projection})
            return collection.aggregate(pipeline)


class BusinessPartners(MongoDataSource):
    def __init__(self, storage, schema):
        super().__init__(
            database="BUSINESS_PARTNER_STORAGE", storage=storage, schema=schema
        )


# NOTE: would like to use context type annotation
# but there's potential problem with that currently
class DataTransfer:
    def __init__(self, source: DataSource, schema: Schema, context):
        self.source = source
        self.schema = schema
        self.context = context

    def to_dataset(self, batch_size: int, name: str):
        raise NotImplementedError


class MongoParquetTransfer(DataTransfer):
    # TODO: as filesystem access is required at some stage,
    # maybe it would be a good idea to use the transfer object like this
    """
    with MongoParquetTransfer(source=source, schema=schema, context=context) as transfer:
        ds = transfer.to_dataset(batch_size=10_000, name='businesspartners')
        ...

    """
    @staticmethod
    def batch_generator(iterable_source, batch_size: int):
        buffer = []
        for record in iterable_source:
            buffer.append(record)
            if len(buffer) == batch_size:
                yield buffer
                buffer = []
        if buffer:
            yield buffer


    def to_dataset(self, batch_size: int, name: str):
        schema_ = self.schema.as_arrow()
        basedir = self.context.workdir / name
        basedir.mkdir(parents=True, exist_ok=True)
        batch_couinter = 0
        for batch in self.batch_generator(self.source.read(), batch_size):
            record_batch = pa.RecordBatch.from_pylist(batch, schema=schema_)
            table = pa.Table.from_batches([record_batch], schema=schema_)
            ds.write_dataset(
                table,
                base_dir=basedir.as_posix(),
                schema=schema_,
                format="parquet",
                existing_data_behavior="overwrite_or_ignore",
            )
            batch_couinter += 1
        return ds.dataset(basedir.as_posix())
