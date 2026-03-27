"""员工相关路由"""

from fastapi import APIRouter, HTTPException, status
from typing import Optional
from models.schemas import DailyReportRequest, APIResponse
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
