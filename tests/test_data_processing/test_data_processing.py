from cdq.data_processing.main import MongoParquetTransfer

def test_batch_generator_batches_correctly():
    iterable = range(7)
    batches = list(MongoParquetTransfer.batch_generator(iterable, 3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6]]

def test_batch_generator_with_exact_batches():
    iterable = range(6)
    batches = list(MongoParquetTransfer.batch_generator(iterable, 3))
    assert batches == [[0, 1, 2], [3, 4, 5]]

def test_batch_generator_empty():
    iterable = []
    batches = list(MongoParquetTransfer.batch_generator(iterable, 2))
    assert batches == []