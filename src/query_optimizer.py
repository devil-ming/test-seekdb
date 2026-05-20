"""
查询优化器模块。
"""

import logging

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """SQL 查询优化器。"""

    def __init__(self):
        self._rules = []
        self._stats = {"total": 0, "optimized": 0}

    def add_rule(self, rule_name: str, priority: int = 0):
        """注册优化规则。"""
        self._rules.append({"name": rule_name, "priority": priority})
        self._rules.sort(key=lambda r: r["priority"], reverse=True)

    def remove_rule(self, rule_name: str) -> bool:
        """移除指定名称的优化规则。"""
        before = len(self._rules)
        self._rules = [r for r in self._rules if r["name"] != rule_name]
        return len(self._rules) < before

    def optimize(self, sql: str) -> str:
        """对 SQL 语句应用优化规则。"""
        self._stats["total"] += 1
        result = sql
        changed = False
        for rule in self._rules:
            new_result = self._apply_rule(result, rule["name"])
            if new_result != result:
                changed = True
            result = new_result
        if changed:
            self._stats["optimized"] += 1
        return result

    def get_stats(self) -> dict:
        """获取优化统计信息。"""
        return dict(self._stats)

    def _apply_rule(self, sql: str, rule_name: str) -> str:
        """应用单条优化规则（简化实现）。"""
        return sql
