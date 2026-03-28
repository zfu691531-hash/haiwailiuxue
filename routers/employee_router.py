"""员工相关路由"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import DailyReportRequest, DailyReportUpdateRequest, PotentialCustomerRequest, DailyReportQueryRequest, APIResponse
from service.employee_service import EmployeeService
import logging

logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter(prefix="/api/employee", tags=["员工管理"])

# 实例化服务层
employee_service = EmployeeService()


@router.post(
    "/report/create",
    response_model=APIResponse,
    summary="员工填写日报",
    description="员工填写工作日报，包含今日工作内容、工作成果、明日计划和遇到的问题"
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
        # 打印调试信息
        logger.info(f"接收到的日报提交请求：department_id={request.department_id}, department_name={request.department_name}")

        # 调用服务层处理业务逻辑
        result = employee_service.save_report(
            employee_id=request.employee_id,
            report_date=request.report_date,
            content=request.content,
            achievements=request.achievements,
            plan_tomorrow=request.plan_tomorrow,
            problems=request.problems,
            status="已提交",  # 自动设置为已提交状态
            department_id=request.department_id,
            department_name=request.department_name
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
    "/report/update",
    response_model=APIResponse,
    summary="员工修改日报",
    description="员工修改已提交的工作日报，可以修改日报标题、内容、工作成果等"
)
async def update_daily_report(request: DailyReportUpdateRequest):
    """
    员工修改日报接口（兼容Dify HTTP节点）

    Args:
        request: 日报更新请求数据
        - employee_id: 员工ID（必填）
        - report_date: 日报日期（必填）
        - content: 今日工作内容（可选）
        - achievements: 工作成果（可选）
        - plan_tomorrow: 明日计划（可选）
        - problems: 遇到的问题（可选）
        - status: 日报状态（可选）
        - department_id: 部门ID（可选）
        - department_name: 部门名称（可选）

    Returns:
        APIResponse: 标准格式的响应结果

    Raises:
        HTTPException: 处理异常时返回错误
    """
    try:
        # 调用服务层处理业务逻辑
        result = employee_service.update_report(
            employee_id=request.employee_id,
            report_date=request.report_date,
            content=request.content,
            achievements=request.achievements,
            plan_tomorrow=request.plan_tomorrow,
            problems=request.problems,
            status=request.status,
            department_id=request.department_id,
            department_name=request.department_name
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


@router.post(
    "/report/query",
    response_model=APIResponse,
    summary="查询日报",
    description="查询员工日报，支持按员工ID、领导员工ID、部门、状态、日期范围等条件查询"
)
async def query_daily_report(
    request: DailyReportQueryRequest
):
    """
    日报查询接口（兼容Dify HTTP节点）

    Args:
        request: 日报查询请求数据
        - employee_id: 员工ID（可选）
        - department_id: 部门ID（可选）
        - department_name: 部门名称（可选）
        - status: 日报状态（可选）
        - start_date: 开始日期（可选）
        - end_date: 结束日期（可选）
        - is_pushed: 是否已推送（可选）

    Returns:
        APIResponse: 标准格式的响应结果，包含日报列表

    Raises:
        HTTPException: 处理异常时返回错误
    """
    try:
        # 调用服务层处理业务逻辑
        result = employee_service.query_reports(
            employee_id=request.employee_id,
            department_id=request.department_id,
            status=request.status,
            start_date=request.start_date,
            end_date=request.end_date,
            is_pushed=request.is_pushed
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
