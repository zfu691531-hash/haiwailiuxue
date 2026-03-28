#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库表结构迁移脚本
为员工表和日报表添加部门字段
"""

import pymysql
import sys

def migrate_database():
    """执行数据库迁移"""
    try:
        # 连接数据库
        print("正在连接数据库...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='dify_customer',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        print("✓ 数据库连接成功")

        # 修改 employee 表
        print("\n正在修改 employee 表...")
        try:
            cursor.execute("ALTER TABLE employee ADD COLUMN IF NOT EXISTS department_id INT DEFAULT NULL COMMENT '部门ID'")
            print("✓ 添加 employee.department_id 成功")
        except pymysql.MySQLError as e:
            if "Duplicate column name" in str(e):
                print("  → employee.department_id 字段已存在，跳过")
            else:
                print(f"  ✗ 添加 employee.department_id 失败: {e}")

        try:
            cursor.execute("ALTER TABLE employee ADD COLUMN IF NOT EXISTS department_name VARCHAR(100) DEFAULT NULL COMMENT '部门名称'")
            print("✓ 添加 employee.department_name 成功")
        except pymysql.MySQLError as e:
            if "Duplicate column name" in str(e):
                print("  → employee.department_name 字段已存在，跳过")
            else:
                print(f"  ✗ 添加 employee.department_name 失败: {e}")

        # 修改 daily_report 表
        print("\n正在修改 daily_report 表...")
        try:
            cursor.execute("ALTER TABLE daily_report ADD COLUMN IF NOT EXISTS department_id INT DEFAULT NULL COMMENT '部门ID'")
            print("✓ 添加 daily_report.department_id 成功")
        except pymysql.MySQLError as e:
            if "Duplicate column name" in str(e):
                print("  → daily_report.department_id 字段已存在，跳过")
            else:
                print(f"  ✗ 添加 daily_report.department_id 失败: {e}")

        try:
            cursor.execute("ALTER TABLE daily_report ADD COLUMN IF NOT EXISTS department_name VARCHAR(100) DEFAULT NULL COMMENT '部门名称'")
            print("✓ 添加 daily_report.department_name 成功")
        except pymysql.MySQLError as e:
            if "Duplicate column name" in str(e):
                print("  → daily_report.department_name 字段已存在，跳过")
            else:
                print(f"  ✗ 添加 daily_report.department_name 失败: {e}")

        # 提交事务
        conn.commit()
        print("\n✓ 所有表结构修改完成！")

        # 验证修改
        print("\n正在验证修改结果...")
        cursor.execute("DESCRIBE employee")
        employee_columns = [row[0] for row in cursor.fetchall()]
        print(f"  employee 表字段: {', '.join(employee_columns)}")

        cursor.execute("DESCRIBE daily_report")
        report_columns = [row[0] for row in cursor.fetchall()]
        print(f"  daily_report 表字段: {', '.join(report_columns)}")

        if 'department_id' in employee_columns and 'department_name' in employee_columns:
            print("\n✓ employee 表迁移成功！")
        else:
            print("\n✗ employee 表迁移失败！")
            return 1

        if 'department_id' in report_columns and 'department_name' in report_columns:
            print("✓ daily_report 表迁移成功！")
        else:
            print("✗ daily_report 表迁移失败！")
            return 1

        cursor.close()
        conn.close()
        return 0

    except Exception as e:
        print(f"\n✗ 迁移失败：{str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(migrate_database())
