"""数据库连接池管理"""

import pymysql
from dbutils.pooled_db import PooledDB
from config.config import DB_CONFIG

# 创建连接池
db_pool = PooledDB(
    creator=pymysql,
    maxconnections=10,  # 最大连接数
    mincached=2,       # 初始化时创建的最少连接数
    maxcached=5,       # 连接池中空闲连接的最大数量
    maxshared=3,       # 连接池中可共享的最大连接数
    blocking=True,     # 连接池中如果没有可用连接后，是否阻塞等待
    **DB_CONFIG
)


def get_connection():
    """从连接池获取连接"""
    return db_pool.connection()


def close_connection(conn):
    """归还连接到连接池"""
    if conn:
        conn.close()
