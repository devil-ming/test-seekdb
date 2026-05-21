"""连接池单元测试。"""

import time
import threading
from src.connection_pool import ConnectionPool


def test_basic_acquire_release():
    """测试基本的获取和释放连接。"""
    pool = ConnectionPool(max_size=5)

    conn = pool.acquire()
    assert conn is not None
    assert pool.active == 1
    assert pool.available == 0

    pool.release(conn)
    assert pool.active == 0
    assert pool.available == 1


def test_pool_reuse():
    """测试连接复用。"""
    pool = ConnectionPool(max_size=5)

    conn1 = pool.acquire()
    pool.release(conn1)

    conn2 = pool.acquire()
    # 应该复用同一个连接
    assert conn2 is conn1


def test_max_size_limit():
    """测试最大连接数限制。"""
    pool = ConnectionPool(max_size=2)

    conn1 = pool.acquire()
    conn2 = pool.acquire()
    assert pool.active == 2

    # 第三个连接应该超时返回 None
    conn3 = pool.acquire(timeout=0.1)
    assert conn3 is None


def test_slow_query_detection():
    """测试慢查询检测。"""
    pool = ConnectionPool(slow_query_threshold=0.5)

    conn = pool.acquire()
    pool.release(conn, elapsed=1.2)

    stats = pool.get_stats()
    assert stats["slow_queries"] == 1


def test_concurrent_access():
    """测试并发访问安全性。"""
    pool = ConnectionPool(max_size=10)
    errors = []

    def worker():
        try:
            for _ in range(20):
                conn = pool.acquire(timeout=1.0)
                if conn:
                    time.sleep(0.01)
                    pool.release(conn)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(errors) == 0
    assert pool.active == 0


def test_reclaim_idle():
    """测试空闲连接回收。"""
    pool = ConnectionPool(max_size=10)

    # 创建多个连接
    conns = [pool.acquire() for _ in range(8)]
    for c in conns:
        pool.release(c)

    assert pool.available == 8

    reclaimed = pool.reclaim_idle()
    assert reclaimed > 0
    assert pool.available <= 5


def test_close_all():
    """测试关闭所有连接。"""
    pool = ConnectionPool(max_size=5)

    conns = [pool.acquire() for _ in range(3)]
    for c in conns:
        pool.release(c)

    pool.close_all()
    assert pool.available == 0
    assert pool.active == 0
