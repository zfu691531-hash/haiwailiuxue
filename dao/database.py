"""数据访问层 - 负责MySQL数据库连接与数据操作"""

import pymysql
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
    
    def insert_customer(self, name: str, creator_id: int = None, creator: str = None, customer_age: int = 0,
                       customer_gender: str = "", customer_fund: str = "",
                       customer_address: str = "", source: str = "", raw_data: str = "",
                       is_target: int = 3, judge_reason: str = "") -> int:
        """
        插入客户信息

        Args:
            name: 客户名称
            creator_id: 创建人ID
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
        (name, creator_id, creator, customer_age, customer_gender, customer_fund,
         customer_address, source, raw_data, is_target, judge_reason, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (name, creator_id, creator, customer_age, customer_gender, customer_fund,
                            customer_address, source, raw_data, is_target, judge_reason, now, now))
        connection.commit()

        customer_id = cursor.lastrowid
        cursor.close()

        return customer_id


class EmployeeDAO:
    """员工数据访问对象"""
    
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
    
    def employee_exists(self, employee_id: int) -> bool:
        """
        检查员工是否存在

        Args:
            employee_id: 员工ID

        Returns:
            True 表示存在，False 表示不存在
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        sql = "SELECT COUNT(*) FROM employee WHERE employee_id = %s"
        cursor.execute(sql, (employee_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        
        return count > 0
    
    def get_employee_name(self, employee_id: int) -> str:
        """
        获取员工姓名

        Args:
            employee_id: 员工ID

        Returns:
            员工姓名，如果不存在则返回空字符串
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        sql = "SELECT name FROM employee WHERE employee_id = %s"
        cursor.execute(sql, (employee_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result[0]
        return ""
    
    def get_employee_role(self, employee_id: int) -> str:
        """
        获取员工角色

        Args:
            employee_id: 员工ID

        Returns:
            员工角色（如 '普通员工', '主管', '经理' 等）
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        sql = "SELECT role FROM employee WHERE employee_id = %s"
        cursor.execute(sql, (employee_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result[0]
        return ""
    
    def check_report_exists(self, employee_id: int, report_date: str) -> bool:
        """
        检查指定日期的日报是否已存在

        Args:
            employee_id: 员工ID
            report_date: 日报日期 (YYYY-MM-DD)

        Returns:
            True 表示已存在，False 表示不存在
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        sql = "SELECT COUNT(*) FROM daily_report WHERE employee_id = %s AND report_date = %s"
        cursor.execute(sql, (employee_id, report_date))
        count = cursor.fetchone()[0]
        cursor.close()
        
        return count > 0
    
    def insert_daily_report(self, employee_id: int, report_date: str, content: str,
                           achievements: str = "", plan_tomorrow: str = "", problems: str = "",
                           status: str = "草稿", is_pushed: int = 0, push_time: str = None) -> int:
        """
        插入日报数据

        Args:
            employee_id: 员工ID
            report_date: 日报日期 (YYYY-MM-DD)
            content: 日报内容
            achievements: 工作成果
            plan_tomorrow: 明日计划
            problems: 遇到的问题
            status: 日报状态
            is_pushed: 是否已推送
            push_time: 推送时间

        Returns:
            插入记录的ID
        """
        connection = self.get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO daily_report
        (employee_id, report_date, content, achievements, plan_tomorrow, problems, status, is_pushed, push_time, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """

        cursor.execute(sql, (employee_id, report_date, content, achievements, plan_tomorrow, problems, status, is_pushed, push_time))
        connection.commit()

        report_id = cursor.lastrowid
        cursor.close()

        return report_id
    
    def get_daily_reports(self, employee_id: int, start_date: str = None,
                          end_date: str = None, limit: int = 100) -> list:
        """
        查询日报数据

        Args:
            employee_id: 员工ID
            start_date: 开始日期 (YYYY-MM-DD)，可选
            end_date: 结束日期 (YYYY-MM-DD)，可选
            limit: 查询数量限制，默认100

        Returns:
            日报数据列表
        """
        connection = self.get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        sql = """
        SELECT id, employee_id, report_date, content, achievements, created_at, updated_at
        FROM daily_report
        WHERE employee_id = %s
        """
        params = [employee_id]
        
        if start_date:
            sql += " AND report_date >= %s"
            params.append(start_date)
        
        if end_date:
            sql += " AND report_date <= %s"
            params.append(end_date)
        
        sql += " ORDER BY report_date DESC, created_at DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        
        return results
    
    def get_subordinates(self, manager_id: int) -> list:
        """
        获取主管下的所有下属

        Args:
            manager_id: 主管ID

        Returns:
            下属员工ID列表
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        sql = "SELECT employee_id FROM employee WHERE manager_id = %s"
        cursor.execute(sql, (manager_id,))
        results = cursor.fetchall()
        cursor.close()
        
        return [row[0] for row in results]
    
    def insert_customer_with_follow(self, name: str, creator: str, customer_age: int,
                                    customer_gender: str, customer_fund: str,
                                    customer_address: str, source: str, raw_data: str,
                                    is_target: int, judge_reason: str,
                                    follow_employee_id: str = None) -> int:
        """
        插入客户信息（包含跟进员工ID）

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
            follow_employee_id: 跟进员工ID

        Returns:
            插入记录的ID
        """
        connection = self.get_connection()
        cursor = connection.cursor()

        sql = """
        INSERT INTO potential_customers
        (customer_name, customer_age, customer_gender, customer_fund,
         customer_address, follow_employee_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (name, customer_age, customer_gender, customer_fund,
                            customer_address, follow_employee_id))
        connection.commit()

        customer_id = cursor.lastrowid
        cursor.close()

        return customer_id
