"""请求响应模型"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import IntEnum


class CustomerTargetType(IntEnum):
    """客户类型枚举"""
    NOT_TARGET = 0      # 非目标客户
    TARGET = 1          # 符合目标客户
    POTENTIAL = 2       # 潜在客户
    INSUFFICIENT_INFO = 3  # 信息不足


class CustomerJudgeRequest(BaseModel):
    """客户研判请求模型"""
    name: str = Field(..., description="客户姓名", min_length=1, max_length=100)
    creator_id: Optional[int] = Field(default=None, description="创建人ID")
    creator: Optional[str] = Field(default=None, description="创建人", max_length=100)
    customer_age: Optional[int] = Field(default=0, description="客户年龄", ge=0, le=120)
    customer_gender: Optional[str] = Field(default="", description="客户性别", max_length=10)
    customer_fund: Optional[str] = Field(default="", description="客户资金情况", max_length=500)
    customer_address: Optional[str] = Field(default="", description="客户地址", max_length=500)
    source: Optional[str] = Field(default="client_judge", description="数据来源", max_length=50)
    raw_data: Optional[str] = Field(default="", description="原始JSON数据", max_length=5000)
    is_target: CustomerTargetType = Field(
        default=CustomerTargetType.INSUFFICIENT_INFO,
        description="客户类型：1=符合目标客户，2=潜在客户，0=非目标客户，3=信息不足"
    )
    judge_reason: Optional[str] = Field(default="", description="判断原因", max_length=1000)
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """验证姓名不能为空"""
        if not v or v.strip() == '':
            raise ValueError('客户姓名不能为空')
        return v.strip()
    
    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "name": "张三",
                "creator_id": 1001,
                "creator": "王经理",
                "customer_age": 35,
                "customer_gender": "男",
                "customer_fund": "500万",
                "customer_address": "北京市朝阳区",
                "source": "client_judge",
                "raw_data": "{\"key\": \"value\"}",
                "is_target": 1,
                "judge_reason": "符合目标客户标准，资金充足"
            }
        }


class DailyReportRequest(BaseModel):
    """日报提交请求模型（符合Dify HTTP节点）"""
    employee_id: int = Field(..., description="员工ID", ge=1)
    report_date: str = Field(..., description="日报日期 (YYYY-MM-DD)", min_length=10, max_length=10)
    content: str = Field(..., description="今日工作内容", min_length=1, max_length=5000)
    achievements: str = Field(default="", description="工作成果", max_length=2000)
    plan_tomorrow: str = Field(default="", description="明日计划", max_length=2000)
    problems: str = Field(default="", description="遇到的问题", max_length=2000)
    is_pushed: int = Field(default=0, description="是否已推送：0=未推送，1=已推送")
    push_time: Optional[str] = Field(default=None, description="推送时间 (YYYY-MM-DD HH:MM:SS)")
    department_id: Optional[int] = Field(default=None, description="部门ID（可选）")
    department_name: Optional[str] = Field(default=None, description="部门名称（可选）", max_length=100)

    @field_validator('content')
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        """验证日报内容不能为空"""
        if not v or v.strip() == '':
            raise ValueError('日报内容不能为空')
        return v.strip()

    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "employee_id": 1001,
                "report_date": "2025-03-26",
                "content": "完成接口开发",
                "achievements": "跑通日报提交接口",
                "plan_tomorrow": "优化权限控制",
                "problems": "无",
                "is_pushed": 0,
                "push_time": None,
                "department_id": 1,
                "department_name": "技术部"
            }
        }


class DailyReportUpdateRequest(BaseModel):
    """日报更新请求模型（符合Dify HTTP节点）"""
    employee_id: int = Field(..., description="员工ID", ge=1)
    report_date: str = Field(..., description="日报日期 (YYYY-MM-DD)", min_length=10, max_length=10)
    content: Optional[str] = Field(default=None, description="今日工作内容（可选）", max_length=5000)
    achievements: Optional[str] = Field(default=None, description="工作成果（可选）", max_length=2000)
    plan_tomorrow: Optional[str] = Field(default=None, description="明日计划（可选）", max_length=2000)
    problems: Optional[str] = Field(default=None, description="遇到的问题（可选）", max_length=2000)
    status: Optional[str] = Field(default=None, description="日报状态（可选）", max_length=20)
    department_id: Optional[int] = Field(default=None, description="部门ID（可选）")
    department_name: Optional[str] = Field(default=None, description="部门名称（可选）", max_length=100)
    
    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "employee_id": 1001,
                "name": "2025-03-26日报（已更新）",
                "report_date": "2025-03-26",
                "content": "完成接口开发并优化",
                "achievements": "跑通日报提交和更新接口",
                "plan_tomorrow": "优化权限控制",
                "problems": "无",
                "status": "已提交"
            }
        }


class PotentialCustomerRequest(BaseModel):
    """意向客户创建请求模型"""
    customer_name: str = Field(..., description="客户姓名", min_length=1, max_length=50)
    customer_age: int = Field(default=None, description="客户年龄", ge=0, le=120)
    customer_gender: str = Field(default="未知", description="客户性别", max_length=10)
    customer_address: str = Field(default=None, description="客户地址", max_length=255)
    customer_fund: str = Field(default=None, description="客户资金情况", max_length=100)
    intention_level: str = Field(default="未知", description="意向等级（高/中/低）", max_length=20)
    intention_product: str = Field(default=None, description="意向产品", max_length=200)
    follow_employee_id: int = Field(..., description="跟进员工ID", ge=1)
    status: str = Field(default="初接触", description="客户状态", max_length=20)
    source: str = Field(default="employee", description="客户来源", max_length=50)
    remark: str = Field(default=None, description="备注信息")

    @field_validator('customer_name')
    @classmethod
    def customer_name_not_empty(cls, v: str) -> str:
        """验证客户姓名不能为空"""
        if not v or v.strip() == '':
            raise ValueError('客户姓名不能为空')
        return v.strip()

    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "customer_name": "李四",
                "customer_age": 35,
                "customer_gender": "男",
                "customer_address": "上海市浦东新区",
                "customer_fund": "300万",
                "intention_level": "高",
                "intention_product": "留学美国",
                "follow_employee_id": 1001,
                "status": "初接触",
                "source": "employee",
                "remark": "有强烈留学意向"
            }
        }


class EmailRequest(BaseModel):
    """邮件请求模型"""
    to: List[str] = []           # 主送邮箱
    cc: List[str] = []           # 抄送邮箱（领导填这里！）
    subject: str                 # 邮件标题
    content: str                 # 报告正文（Markdown）
    content_type: str = "text/markdown"  # 内容格式


class DailyReportQueryRequest(BaseModel):
    """日报查询请求模型（符合Dify HTTP节点）"""
    employee_id: Optional[int] = Field(default=None, description="员工ID（可选，不传则查询所有）")
    department_id: Optional[int] = Field(default=None, description="部门ID（可选）")
    department_name: Optional[str] = Field(default=None, description="部门名称（可选）")
    status: Optional[str] = Field(default=None, description="日报状态（可选，如：草稿、已提交、已审核）")
    start_date: Optional[str] = Field(default=None, description="开始日期 (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="结束日期 (YYYY-MM-DD)")
    is_pushed: Optional[int] = Field(default=None, description="是否已推送（可选，0=未推送，1=已推送）")

    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "employee_id": 1001,
                "department_id": 1,
                "department_name": "技术部",
                "status": "已提交",
                "start_date": "2025-03-01",
                "end_date": "2025-03-31",
                "is_pushed": 1
            }
        }


class SQLExecuteRequest(BaseModel):
    """SQL执行请求模型（符合Dify HTTP节点）"""
    sql: str = Field(..., description="SQL查询语句（仅支持SELECT查询）", min_length=1)
    
    @field_validator('sql')
    @classmethod
    def validate_sql(cls, v: str) -> str:
        """验证SQL语句是否合法"""
        sql_upper = v.strip().upper()
        
        # 只允许SELECT查询，防止数据库被修改
        if not sql_upper.startswith('SELECT'):
            raise ValueError('仅支持SELECT查询，不允许使用其他SQL语句')
        
        # 检查危险关键字
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE', 'EXEC']
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise ValueError(f'SQL语句包含危险关键字：{keyword}')
        
        return v.strip()
    
    class Config:
        """Pydantic模型配置"""
        json_schema_extra = {
            "example": {
                "sql": "SELECT * FROM employee WHERE role = '普通员工' LIMIT 10"
            }
        }


class APIResponse(BaseModel):
    """统一API响应模型"""
    code: int = Field(..., description="响应状态码：200=成功，500=失败")
    msg: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(default=None, description="响应数据")
