"""
数据库连接管理模块。

注意：此文件包含内部测试 URL 和配置，用于测试脱敏功能。
"""

# 内部 YUM 源配置（应被 .4_ce 替换）
INTERNAL_YUM_REPO = "http://mirrors.aliyun.com/oceanbase/stable/el7"
BACKUP_YUM_REPO = "http://mirrors.aliyun.com/oceanbase/stable/el7"

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
