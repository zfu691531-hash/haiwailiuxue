"""FastAPI应用主入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="海外留学客户管理系统",
    description="客户研判、员工管理、邮件发送等功能",
    version="2.0.0"
)

# 配置CORS中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 导入路由（延迟导入避免循环依赖）
from routers.employee_router import router as employee_router
from routers.email_router import router as email_router
from routers.customer_router import router as customer_router
from routers.report_router import router as report_router

# 注册路由
app.include_router(employee_router)
app.include_router(email_router)
app.include_router(customer_router)
app.include_router(report_router)  # Dify兼容的日报接口

# 健康检查接口
@app.get("/", summary="健康检查", description="检查服务是否正常运行")
async def root():
    """健康检查接口"""
    return {
        "code": 200,
        "msg": "服务运行正常",
        "data": {
            "service": "海外留学客户管理系统",
            "status": "running",
            "version": "2.0.0"
        }
    }


@app.get("/health", summary="健康检查", description="检查服务是否正常运行")
async def health():
    """健康检查接口"""
    return {
        "code": 200,
        "msg": "服务运行正常",
        "data": {
            "service": "海外留学客户管理系统",
            "status": "running",
            "version": "2.0.0"
        }
    }
