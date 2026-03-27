"""员工相关路由"""

from fastapi import APIRouter, HTTPException, status
from typing import Optional
from models.schemas import DailyReportRequest, PotentialCustomerRequest, APIResponse
from service.employee_service import EmployeeService

# 创建路由
router = APIRouter(prefix="/api/employee", tags=["员工管理"])

# 实例化服务层
employee_service = EmployeeService()


@router.post(
    "/report/create",
    response_model=APIResponse,
    summary="员工填写日报",
    description="员工填写工作日报，包含日报标题、今日工作内容、工作成果、明日计划和遇到的问题"
)
async def create_daily_report(request: DailyReportRequest):
    """
    员工填写日报接口（兼容Dify HTTP节点）
    
    Args:
        request: 日报填写请求数据
        
    Returns:
        APIResponse: 标准格式的响应结果
        
    Raises:
        HTTPException: 处理异常时返回500错误
    """
    try:
        # 调用服务层处理业务逻辑
        result = employee_service.save_report(
            employee_id=request.employee_id,
            title=request.name,  # name字段作为日报标题
            report_date=request.report_date,
            content=request.content,
            achievements=request.achievements,
            plan_tomorrow=request.plan_tomorrow,
            problems=request.problems,
            status="已提交"  # 自动设置为已提交状态
        )
        
        # 如果处理失败，返回500错误
        if result['code'] != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result['msg']
            )
        
        return APIResponse(
            code=result['code'],
            msg=result['msg'],
            data=result['data']
        )
        
    except ValueError as ve:
        # 参数验证异常
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'参数验证失败：{str(ve)}'
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 其他异常
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'服务器内部错误：{str(e)}'
        )


@router.post(
    "/potential/customer/create",
    response_model=APIResponse,
    summary="员工创建意向客户",
    description="员工创建意向客户，包含客户基本信息、意向等级、意向产品等"
)
async def create_potential_customer(request: PotentialCustomerRequest):
    """
    员工创建意向客户接口

    Args:
        request: 意向客户创建请求数据
        - customer_name: 客户姓名（必填）
        - customer_age: 客户年龄（选填）
        - customer_gender: 客户性别（选填，默认"未知"）
        - customer_address: 客户地址（选填）
        - customer_fund: 客户资金情况（选填）
        - intention_level: 意向等级（选填，默认"未知"）
        - intention_product: 意向产品（选填）
        - follow_employee_id: 跟进员工ID（必填）
        - status: 客户状态（选填，默认"初接触"）
        - source: 客户来源（选填，默认"employee"）
        - remark: 备注信息（选填）

    Returns:
        APIResponse: 标准格式的响应结果

    Raises:
        HTTPException: 处理异常时返回错误
    """
    try:
        # 调用服务层处理业务逻辑
        result = employee_service.create_potential_customer(
            customer_name=request.customer_name,
            customer_age=request.customer_age,
            customer_gender=request.customer_gender,
            customer_address=request.customer_address,
            customer_fund=request.customer_fund,
            intention_level=request.intention_level,
            intention_product=request.intention_product,
            follow_employee_id=request.follow_employee_id,
            status=request.status,
            source=request.source,
            remark=request.remark
        )

        # 如果处理失败，返回错误
        if result['code'] != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['msg']
            )

        return APIResponse(
            code=result['code'],
            msg=result['msg'],
            data=result['data']
        )

    except ValueError as ve:
        # 参数验证异常
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'参数验证失败：{str(ve)}'
        )
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 其他异常
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'服务器内部错误：{str(e)}'
        )
