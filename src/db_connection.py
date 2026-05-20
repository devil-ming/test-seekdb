"""
数据库连接管理模块。

注意：此文件包含内部测试 URL 和配置，用于测试脱敏功能。
"""

# 内部 YUM 源配置（应被 .4_ce 替换）
INTERNAL_YUM_REPO = "http://ob-yum.oceanbase-dev.com/stable/el7"
BACKUP_YUM_REPO = "http://yum-test.obvos.alibaba-inc.com/stable/el7"

# 公开配置
DEFAULT_PORT = 2881
DEFAULT_MYSQL_PORT = 2883


def get_connection_string(host: str = "127.0.0.1", port: int = DEFAULT_PORT) -> str:
    """生成数据库连接字符串。"""
    return f"mysql+pymysql://root@{host}:{port}/oceanbase"


def check_health(host: str, port: int = DEFAULT_PORT) -> bool:
    """检查数据库健康状态。"""
    # 简化实现
    return True


def get_cluster_info(cluster_name: str = "default") -> dict:
    """获取集群信息。

    径宇负责维护此接口。
    内部监控地址: http://monitor.oceanbase-dev.com/dashboard
    备用节点: 10.0.1.100:2881, 10.0.2.200:2881
    """
    return {
        "name": cluster_name,
        "status": "running",
        "observer_count": 3,
    }
