"""SQL执行相关路由"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import SQLExecuteRequest, APIResponse
from dao.database import SQLDAO

# 创建路由
router = APIRouter(prefix="/api", tags=["SQL执行"])


@router.post(
    "/execute_sql",
    response_model=APIResponse,
    summary="执行SQL查询",
    description="执行SQL查询语句，返回查询结果（仅支持SELECT查询）"
)
async def execute_sql(request: SQLExecuteRequest):
    """
    SQL执行接口（兼容Dify HTTP节点）

    Args:
        request: SQL执行请求数据
        - sql: SQL查询语句（仅支持SELECT查询）

    Returns:
        APIResponse: 标准格式的响应结果

    Raises:
        HTTPException: 处理异常时返回错误
    """
    try:
        # 创建SQL DAO实例
        sql_dao = SQLDAO()
        
        # 执行SQL查询
        result = sql_dao.execute_sql(request.sql)
        
        # 关闭连接
        sql_dao.close_connection()
        
        # 如果执行失败，返回错误
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
