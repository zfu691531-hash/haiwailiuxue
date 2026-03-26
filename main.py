"""主入口文件 - 启动FastAPI应用"""

import uvicorn
from api.customer_api import app


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        log_level="info",
        reload=False  # 生产环境设为False，开发环境可设为True以支持热重载
    )
