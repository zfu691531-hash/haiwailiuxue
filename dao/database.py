"""数据访问层 - 负责MySQL数据库连接与数据操作"""

import pymysql
import json
from datetime import datetime
from config.config import DB_CONFIG


class CustomerDAO:
    """客户数据访问对象"""
    
    def __init__(self):
        self.connection = None
    
    def get_connection(self):
        """获取数据库连接"""
        if not self.connection:
            self.connection = pymysql.connect(**DB_CONFIG)
        return self.connection
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def insert_customer(self, name: str, creator: str, customer_age: int, 
                       customer_gender: str, customer_fund: str, 
                       customer_address: str, source: str, raw_data: str, 
                       is_target: int, judge_reason: str) -> int:
        """
        插入客户信息
        
        Args:
            name: 客户名称
            creator: 创建人
            customer_age: 客户年龄
            customer_gender: 客户性别
            customer_fund: 客户资金
            customer_address: 客户地址
            source: 数据来源
            raw_data: 原始JSON数据
            is_target: 是否为目标客户 (1=符合目标客户，2=潜在客户，0=非目标客户，3=信息不足)
            judge_reason: 判断原因
            
        Returns:
            插入记录的ID
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        now = datetime.now()
        
        sql = """
        INSERT INTO customer_info 
        (name, creator, customer_age, customer_gender, customer_fund, 
         customer_address, source, raw_data, is_target, judge_reason, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(sql, (name, creator, customer_age, customer_gender, customer_fund, 
                                customer_address, source, raw_data, is_target, judge_reason, now, now))
            connection.commit()
            
            customer_id = cursor.lastrowid
            cursor.close()
            
            return customer_id
        except Exception as e:
            connection.rollback()
            raise
