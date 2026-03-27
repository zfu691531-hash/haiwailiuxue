"""服务层 - 员工相关业务逻辑"""

from typing import Dict, Any
from dao.database import EmployeeDAO


class EmployeeService:
    """员工服务类"""
    
    def __init__(self):
        self.dao = EmployeeDAO()
    
    def save_report(self, employee_id: int, title: str, report_date: str,
                   content: str, achievements: str = "", plan_tomorrow: str = "",
                   problems: str = "", status: str = "草稿", is_pushed: int = 0,
                   push_time: str = None) -> Dict[str, Any]:
        """
        保存员工日报

        Args:
            employee_id: 员工ID
            title: 日报标题
            report_date: 日报日期 (YYYY-MM-DD)
            content: 日报内容
            achievements: 工作成果
            plan_tomorrow: 明日计划
            problems: 遇到的问题
            status: 日报状态
            is_pushed: 是否已推送
            push_time: 推送时间

        Returns:
            包含处理结果的字典（code, msg, data）
        """
        try:
            # 检查员工是否存在并获取员工姓名
            if not self.dao.employee_exists(employee_id):
                return {
                    'code': 400,
                    'msg': f'员工 ID {employee_id} 不存在',
                    'data': None
                }
            
            # 获取员工姓名
            employee_name = self.dao.get_employee_name(employee_id)
            
            # 如果不是草稿状态，检查是否重复提交
            if status != "草稿":
                if self.dao.check_report_exists(employee_id, report_date):
                    return {
                        'code': 400,
                        'msg': f'员工 {employee_id} 在 {report_date} 的日报已存在，请勿重复提交',
                        'data': None
                    }
            
            # 将日报标题和工作内容合并到 content 字段
            full_content = f"【{title}】\n\n{content}"
            
            # 插入日报数据
            report_id = self.dao.insert_daily_report(
                employee_id=employee_id,
                report_date=report_date,
                content=full_content,  # 合并标题和内容
                achievements=achievements,
                plan_tomorrow=plan_tomorrow,
                problems=problems,
                status=status,
                is_pushed=is_pushed,
                push_time=push_time
            )
            
            return {
                'code': 200,
                'msg': f'员工 {employee_id} 的日报已成功保存',
                'data': {
                    'report_id': report_id,
                    'employee_id': employee_id,
                    'employee_name': employee_name,
                    'report_date': report_date,
                    'status': status
                }
            }
            
        except Exception as e:
            return {
                'code': 500,
                'msg': f'保存日报失败：{str(e)}',
                'data': None
            }
    
    def query_reports(self, employee_id: int = None, leader_employee_id: int = None,
                     start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        查询日报数据

        Args:
            employee_id: 员工ID（员工查自己的日报）
            leader_employee_id: 领导员工ID（领导查下属的日报）
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)

        Returns:
            包含处理结果的字典（code, msg, data）
        """
        try:
            reports_data = []
            
            # 如果传入了领导员工ID，则查询该领导下的所有下属的日报
            if leader_employee_id:
                # 获取领导下的所有下属员工ID
                subordinates = self.dao.get_subordinates(leader_employee_id)
                
                # 对每个下属员工查询日报
                for subordinate_id in subordinates:
                    reports = self.dao.get_daily_reports(
                        employee_id=subordinate_id,
                        start_date=start_date,
                        end_date=end_date
                    )
                    reports_data.extend(reports)
            
            # 如果只传入了员工ID，则查询该员工自己的日报
            elif employee_id:
                reports = self.dao.get_daily_reports(
                    employee_id=employee_id,
                    start_date=start_date,
                    end_date=end_date
                )
                reports_data.extend(reports)
            
            else:
                return {
                    'code': 400,
                    'msg': '请至少提供 employee_id 或 leader_employee_id 参数',
                    'data': None
                }
            
            return {
                'code': 200,
                'msg': '日报查询成功',
                'data': {
                    'reports': reports_data,
                    'total': len(reports_data)
                }
            }
            
        except Exception as e:
            return {
                'code': 500,
                'msg': f'查询日报失败：{str(e)}',
                'data': None
            }
    
    def create_potential_customer(self, customer_name: str, customer_age: int,
                                  customer_gender: str, customer_address: str,
                                  customer_fund: str, follow_employee_id: str,
                                  raw_data: str = None) -> Dict[str, Any]:
        """
        创建潜在客户
        
        Args:
            customer_name: 客户姓名
            customer_age: 客户年龄
            customer_gender: 客户性别
            customer_address: 客户地址
            customer_fund: 客户资金情况
            follow_employee_id: 跟进员工ID
            raw_data: 原始JSON数据
            
        Returns:
            包含处理结果的字典（code, msg, data）
        """
        try:
            # 检查跟进员工是否存在
            if not self.dao.employee_exists(follow_employee_id):
                return {
                    'code': 400,
                    'msg': f'跟进员工 ID {follow_employee_id} 不存在',
                    'data': None
                }
            
            # 插入客户信息
            customer_id = self.dao.insert_customer_with_follow(
                name=customer_name,
                creator=follow_employee_id,
                customer_age=customer_age,
                customer_gender=customer_gender,
                customer_fund=customer_fund,
                customer_address=customer_address,
                source='employee_potential',
                raw_data=raw_data or str({
                    'customer_name': customer_name,
                    'customer_age': customer_age,
                    'customer_gender': customer_gender,
                    'customer_address': customer_address,
                    'customer_fund': customer_fund,
                    'follow_employee_id': follow_employee_id
                }),
                is_target=2,  # 潜在客户
                judge_reason='员工推荐的潜在客户',
                follow_employee_id=follow_employee_id
            )
            
            return {
                'code': 200,
                'msg': f'潜在客户创建成功，客户ID: {customer_id}',
                'data': {
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'follow_employee_id': follow_employee_id
                }
            }
            
        except Exception as e:
            return {
                'code': 500,
                'msg': f'创建潜在客户失败：{str(e)}',
                'data': None
            }
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        self.dao.close_connection()
