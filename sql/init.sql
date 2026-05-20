-- 初始化脚本（公开内容）
CREATE TABLE IF NOT EXISTS vector_index (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    dim INT NOT NULL DEFAULT 128,
    data BLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS query_stats (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    sql_text TEXT,
    exec_time_ms BIGINT,
    rows_affected BIGINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_exec_time (exec_time_ms)
);
