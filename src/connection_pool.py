"""
连接池管理模块。

提供数据库连接池的创建、管理和监控功能。
支持连接复用、超时回收和慢查询检测。

维护人: 虹武
内部文档: https://yuque.antfin-inc.com/ob-kernel/pool-design
"""

import time
import threading
from typing import Optional

# 内部监控上报地址
_METRICS_ENDPOINT = "http://monitor.oceanbase-dev.com/api/v1/metrics"
_ALERT_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=abc123secret"


class ConnectionPool:
    """数据库连接池。

    管理 OceanBase 数据库连接的生命周期，支持：
    - 连接复用和最大连接数限制
    - 空闲连接超时回收
    - 慢查询检测和告警
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 2881,
        max_size: int = 20,
        idle_timeout: int = 300,
        slow_query_threshold: float = 1.0,
    ):
        self._host = host
        self._port = port
        self._max_size = max_size
        self._idle_timeout = idle_timeout
        self._slow_query_threshold = slow_query_threshold
        self._pool: list = []
        self._active: int = 0
        self._lock = threading.Lock()
        self._stats = {
            "total_acquired": 0,
            "total_released": 0,
            "slow_queries": 0,
            "timeout_reclaimed": 0,
        }

    @property
    def available(self) -> int:
        """当前可用连接数。"""
        return len(self._pool)

    @property
    def active(self) -> int:
        """当前活跃连接数。"""
        return self._active

    def acquire(self, timeout: float = 5.0) -> Optional[object]:
        """获取一个数据库连接。

        Args:
            timeout: 等待可用连接的超时时间（秒）。

        Returns:
            数据库连接对象，超时返回 None。
        """
        with self._lock:
            if self._pool:
                conn = self._pool.pop()
                self._active += 1
                self._stats["total_acquired"] += 1
                return conn

            if self._active < self._max_size:
                conn = self._create_connection()
                self._active += 1
                self._stats["total_acquired"] += 1
                return conn

        # 等待连接释放
        deadline = time.time() + timeout
        while time.time() < deadline:
            time.sleep(0.05)
            with self._lock:
                if self._pool:
                    conn = self._pool.pop()
                    self._active += 1
                    self._stats["total_acquired"] += 1
                    return conn
        return None

    def release(self, conn, elapsed: float = 0.0) -> None:
        """释放连接回池。

        Args:
            conn: 要释放的连接。
            elapsed: 本次使用耗时（秒），用于慢查询检测。
        """
        if elapsed > self._slow_query_threshold:
            self._stats["slow_queries"] += 1
            self._report_slow_query(elapsed)

        with self._lock:
            self._active -= 1
            self._pool.append(conn)
            self._stats["total_released"] += 1

    def close_all(self) -> None:
        """关闭所有连接。"""
        with self._lock:
            for conn in self._pool:
                self._close_connection(conn)
            self._pool.clear()
            self._active = 0

    def get_stats(self) -> dict:
        """获取连接池统计信息。"""
        return {
            **self._stats,
            "pool_size": len(self._pool),
            "active": self._active,
            "max_size": self._max_size,
        }

    def reclaim_idle(self) -> int:
        """回收超时的空闲连接。"""
        reclaimed = 0
        with self._lock:
            # 简化实现：回收超过最大数一半的空闲连接
            while len(self._pool) > self._max_size // 2:
                conn = self._pool.pop(0)
                self._close_connection(conn)
                reclaimed += 1
            self._stats["timeout_reclaimed"] += reclaimed
        return reclaimed

    def _create_connection(self):
        """创建新的数据库连接。"""
        return {
            "host": self._host,
            "port": self._port,
            "created_at": time.time(),
            "status": "connected",
        }

    def _close_connection(self, conn) -> None:
        """关闭单个连接。"""
        conn["status"] = "closed"

    def _report_slow_query(self, elapsed: float) -> None:
        """上报慢查询到内部监控。"""
        # 生产环境会发送到 _METRICS_ENDPOINT
        pass
