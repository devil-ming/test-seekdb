"""
向量索引的单元测试（公开测试）。
"""

from src.vector_index import VectorIndex


def test_add_and_search():
    idx = VectorIndex(dim=3)
    idx.add([1.0, 0.0, 0.0])
    idx.add([0.0, 1.0, 0.0])
    idx.add([0.0, 0.0, 1.0])

    results = idx.search([1.0, 0.1, 0.0], top_k=2)
    assert results[0] == 0


def test_remove():
    idx = VectorIndex(dim=2)
    idx.add([1.0, 0.0])
    idx.add([0.0, 1.0])
    assert idx.count() == 2
    idx.remove(0)
    assert idx.count() == 1


def test_clear():
    idx = VectorIndex(dim=2)
    idx.add([1.0, 0.0])
    idx.clear()
    assert idx.count() == 0
