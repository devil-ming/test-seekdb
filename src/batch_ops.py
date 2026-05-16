"""
批量操作模块 — 支持向量索引的批量导入导出。
"""

from src.vector_index import VectorIndex


class BatchImporter:
    """批量导入向量数据。"""

    def __init__(self, index: VectorIndex):
        self._index = index
        self._imported = 0

    def import_from_list(self, vectors: list[list[float]]) -> int:
        """从列表批量导入向量。

        Returns:
            成功导入的数量。
        """
        count = 0
        for vec in vectors:
            try:
                self._index.add(vec)
                count += 1
            except ValueError:
                continue
        self._imported += count
        return count

    @property
    def total_imported(self) -> int:
        return self._imported


class BatchExporter:
    """批量导出向量数据。"""

    def __init__(self, index: VectorIndex):
        self._index = index

    def export_to_list(self) -> list[list[float]]:
        """将索引中的所有向量导出为列表。"""
        return list(self._index._data)
