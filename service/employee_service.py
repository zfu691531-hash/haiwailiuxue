"""服务层 - 员工相关业务逻辑"""

from typing import Dict, Any
from dao.database import EmployeeDAO


class EmployeeService:
    """员工服务类"""
    
    def __init__(self):
        self.dao = EmployeeDAO()

    def save_report(
        self, employee_id: int, report_date: str, content: str,
        achievements: str = "", plan_tomorrow: str = "",
        problems: str = "", status: str = "草稿", is_pushed: int = 0,
        push_time: str = None, department_id: int = None, department_name: str = None
    ) -> Dict[str, Any]:
        """
        保存员工日报

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
            department_id: 部门ID（可选）
            department_name: 部门名称（可选）

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

            # 插入日报数据（直接存储 content）
            report_id = self.dao.insert_daily_report(
                employee_id=employee_id,
                report_date=report_date,
                content=content,
                achievements=achievements,
                plan_tomorrow=plan_tomorrow,
                problems=problems,
                status=status,
                is_pushed=is_pushed,
                push_time=push_time,
                department_id=department_id,
                department_name=department_name
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

    def query_reports(self, employee_id: int = None,
                      department_id: int = None, status: str = None,
                      start_date: str = None, end_date: str = None,
                      is_pushed: int = None) -> Dict[str, Any]:
        """
        查询日报数据

        Args:
            employee_id: 员工ID（员工查自己的日报）
            department_id: 部门ID（可选）
            status: 日报状态（可选）
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            is_pushed: 是否已推送（可选）

        Returns:
            包含处理结果的字典（code, msg, data）
        """
        try:
            reports_data = []

            # 根据员工ID或其他条件查询
            reports = self.dao.get_daily_reports(
                employee_id=employee_id,
                department_id=department_id,
                status=status,
                start_date=start_date,
                end_date=end_date,
                is_pushed=is_pushed
            )
            reports_data.extend(reports)

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

    def update_report(self, employee_id: int, report_date: str,
                    content: str = None,
                    achievements: str = None, plan_tomorrow: str = None,
                    problems: str = None, status: str = None,
                    department_id: int = None, department_name: str = None) -> Dict[str, Any]:
        """
        更新员工日报

        Args:
            employee_id: 员工ID（必填）
            report_date: 日报日期 (YYYY-MM-DD)（必填）
            content: 日报内容（可选）
            achievements: 工作成果（可选）
            plan_tomorrow: 明日计划（可选）
            problems: 遇到的问题（可选）
            status: 日报状态（可选）
            department_id: 部门ID（可选）
            department_name: 部门名称（可选）

        Returns:
            包含处理结果的字典（code, msg, data）
        """
        try:
            # 检查员工是否存在
            if not self.dao.employee_exists(employee_id):
                return {
                    'code': 400,
                    'msg': f'员工 ID {employee_id} 不存在',
                    'data': None
                }

            # 检查该员工在指定日期的日报是否存在
            if not self.dao.check_report_exists(employee_id, report_date):
                return {
                    'code': 404,
                    'msg': f'员工 {employee_id} 在 {report_date} 的日报不存在',
                    'data': None
                }

            # 构建只包含非空字段的更新数据
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if achievements is not None:
                update_data['achievements'] = achievements
            if plan_tomorrow is not None:
                update_data['plan_tomorrow'] = plan_tomorrow
            if problems is not None:
                update_data['problems'] = problems
            if status is not None:
                update_data['status'] = status
            if department_id is not None:
                update_data['department_id'] = department_id
            if department_name is not None:
                update_data['department_name'] = department_name

            # 如果没有需要更新的字段，直接返回成功
            if not update_data:
                return {
                    'code': 200,
                    'msg': '没有需要更新的字段',
                    'data': {
                        'employee_id': employee_id,
                        'report_date': report_date
                    }
                }

            # 更新日报数据
            success = self.dao.update_daily_report(
                employee_id=employee_id,
                report_date=report_date,
                update_data=update_data
            )

            if not success:
                return {
                    'code': 500,
                    'msg': f'更新日报失败',
                    'data': None
                }

            # 查询更新后的日报ID
            reports = self.dao.get_daily_reports(employee_id=employee_id, start_date=report_date, end_date=report_date, limit=1)
            report_id = reports[0]['id'] if reports else None

            return {
                'code': 200,
                'msg': f'员工 {employee_id} 在 {report_date} 的日报已成功更新',
                'data': {
                    'report_id': report_id,
                    'employee_id': employee_id,
                    'report_date': report_date
                }
            }

        except Exception as e:
            return {
                'code': 500,
                'msg': f'更新日报失败：{str(e)}',
                'data': None
            }
    
    def create_potential_customer(self, customer_name: str, customer_age: int = None,
                                  customer_gender: str = "未知", customer_address: str = None,
                                  customer_fund: str = None, intention_level: str = "未知",
                                  intention_product: str = None, follow_employee_id: int = None,
                                  status: str = "初接触", source: str = "employee",
                                  remark: str = None) -> Dict[str, Any]:
        """
        创建意向客户

        Args:
            customer_name: 客户姓名
            customer_age: 客户年龄
            customer_gender: 客户性别
            customer_address: 客户地址
            customer_fund: 客户资金情况
            intention_level: 意向等级
            intention_product: 意向产品
            follow_employee_id: 跟进员工ID
            status: 客户状态
            source: 客户来源
            remark: 备注信息

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
            customer_id = self.dao.insert_potential_customer(
                customer_name=customer_name,
                customer_age=customer_age,
                customer_gender=customer_gender,
                customer_fund=customer_fund,
                customer_address=customer_address,
                intention_level=intention_level,
                intention_product=intention_product,
                follow_employee_id=follow_employee_id,
                status=status,
                source=source,
                remark=remark
            )

            return {
                'code': 200,
                'msg': f'意向客户创建成功，客户ID: {customer_id}',
                'data': {
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'follow_employee_id': follow_employee_id,
                    'status': status
                }
            }

        except Exception as e:
            return {
                'code': 500,
                'msg': f'创建意向客户失败：{str(e)}',
                'data': None
            }
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        self.dao.close_connection()
