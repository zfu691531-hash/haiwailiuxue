"""客户相关路由"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import CustomerJudgeRequest, APIResponse
from service.customer_service import CustomerService

# 创建路由
router = APIRouter(prefix="/api/customer", tags=["客户管理"])

# 实例化服务层
customer_service = CustomerService()


@router.post(
    "/judge",
    response_model=APIResponse,
    summary="保存客户研判数据",
    description="接收Dify工作流传来的客户研判数据并写入MySQL数据库"
)
async def save_customer_judge(request: CustomerJudgeRequest):
    """
    保存客户研判数据接口
    
    Args:
        request: 客户研判请求数据
        
    Returns:
        APIResponse: 标准格式的响应结果
        
    Raises:
        HTTPException: 处理异常时返回500错误
    """
    try:
        # 将请求数据转换为字典
        customer_data = {
            'name': request.name,
            'creator_id': request.creator_id,
            'creator': request.creator,
            'customer_age': request.customer_age,
            'customer_gender': request.customer_gender,
            'customer_fund': request.customer_fund,
            'customer_address': request.customer_address,
            'source': request.source or 'client_judge',
            'raw_data': request.raw_data,
            'is_target': request.is_target.value,
            'judge_reason': request.judge_reason
        }
        
        # 调用服务层处理业务逻辑
        result = customer_service.save_customer_judge(customer_data)
        
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
