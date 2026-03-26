"""API层 - FastAPI接口定义"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import IntEnum
from service.customer_service import CustomerService


# 创建FastAPI应用实例
app = FastAPI(
    title="客户研判数据API",
    description="接收Dify工作流传来的客户研判数据并写入MySQL数据库",
    version="1.0.0"
)

# 配置CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


class CustomerTargetType(IntEnum):
    """客户类型枚举"""
    NOT_TARGET = 0      # 非目标客户
    TARGET = 1          # 符合目标客户
    POTENTIAL = 2       # 潜在客户
    INSUFFICIENT_INFO = 3  # 信息不足


class CustomerJudgeRequest(BaseModel):
    """客户研判请求模型"""
    name: str = Field(..., description="客户姓名", min_length=1, max_length=100)
    customer_age: Optional[int] = Field(default=0, description="客户年龄", ge=0, le=120)
    customer_gender: Optional[str] = Field(default="", description="客户性别", max_length=10)
    customer_fund: Optional[str] = Field(default="", description="客户资金情况", max_length=500)
    customer_address: Optional[str] = Field(default="", description="客户地址", max_length=500)
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
                "customer_age": 35,
                "customer_gender": "男",
                "customer_fund": "500万",
                "customer_address": "北京市朝阳区",
                "raw_data": "{\"key\": \"value\"}",
                "is_target": 1,
                "judge_reason": "符合目标客户标准，资金充足"
            }
        }


class APIResponse(BaseModel):
    """统一API响应模型"""
    code: int = Field(..., description="响应状态码：200=成功，500=失败")
    msg: str = Field(..., description="响应消息")
    data: Optional[dict] = Field(default=None, description="响应数据")


# 实例化服务层
customer_service = CustomerService()


@app.post(
    "/api/save_customer_judge",
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
            'customer_age': request.customer_age,
            'customer_gender': request.customer_gender,
            'customer_fund': request.customer_fund,
            'customer_address': request.customer_address,
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


@app.get("/", summary="健康检查", description="检查服务是否正常运行")
async def root():
    """健康检查接口"""
    return {
        "code": 200,
        "msg": "服务运行正常",
        "data": {
            "service": "客户研判数据API",
            "status": "running"
        }
    }


@app.get("/health", summary="健康检查", description="检查服务是否正常运行")
async def health():
    """健康检查接口"""
    return {
        "code": 200,
        "msg": "服务运行正常",
        "data": {
            "service": "客户研判数据API",
            "status": "running"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
