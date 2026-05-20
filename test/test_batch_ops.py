"""
批量操作的测试用例。
"""

from src.vector_index import VectorIndex
from src.batch_ops import BatchImporter, BatchExporter


def test_batch_import():
    idx = VectorIndex(dim=2)
    importer = BatchImporter(idx)
    count = importer.import_from_list([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
    ])
    assert count == 3
    assert importer.total_imported == 3
    assert idx.count() == 3


def test_batch_import_invalid():
    idx = VectorIndex(dim=2)
    importer = BatchImporter(idx)
    count = importer.import_from_list([
        [1.0, 0.0],
        [1.0, 2.0, 3.0],  # wrong dim
        [0.0, 1.0],
    ])
    assert count == 2


def test_batch_export():
    idx = VectorIndex(dim=2)
    idx.add([1.0, 0.0])
    idx.add([0.0, 1.0])
    exporter = BatchExporter(idx)
    data = exporter.export_to_list()
    assert len(data) == 2
    assert exporter.export_count() == 2
