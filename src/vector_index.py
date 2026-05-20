"""
OceanBase 向量索引模块 — 公开功能代码。

这个文件模拟一个正常的业务代码文件，包含可以公开的内容。
"""


class VectorIndex:
    """向量索引管理器。"""

    def __init__(self, dim: int = 128):
        self.dim = dim
        self._data = []

    def add(self, vector: list[float]) -> int:
        """添加向量到索引。"""
        if len(vector) != self.dim:
            raise ValueError(f"Expected dim={self.dim}, got {len(vector)}")
        self._data.append(vector)
        return len(self._data) - 1

    def search(self, query: list[float], top_k: int = 10) -> list[int]:
        """搜索最近邻向量。"""
        if not self._data:
            return []
        # 简化实现：暴力搜索
        distances = []
        for i, vec in enumerate(self._data):
            dist = sum((a - b) ** 2 for a, b in zip(query, vec))
            distances.append((dist, i))
        distances.sort()
        return [idx for _, idx in distances[:top_k]]

    def remove(self, index: int) -> None:
        """从索引中删除向量。"""
        if 0 <= index < len(self._data):
            self._data.pop(index)

    def count(self) -> int:
        """返回索引中的向量数量。"""
        return len(self._data)

    def clear(self) -> None:
        """清空索引。"""
        self._data.clear()
