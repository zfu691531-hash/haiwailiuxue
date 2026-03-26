# 客户研判数据API

基于FastAPI的后端接口，用于接收Dify工作流传来的客户研判数据并写入MySQL数据库。

## 功能特性

- ✅ RESTful API设计
- ✅ 自动参数校验（Pydantic）
- ✅ 完善的异常处理
- ✅ 支持CORS跨域
- ✅ 标准JSON响应格式
- ✅ 完整的代码注释
- ✅ 适配Dify工作流HTTP节点

## 技术栈

- **FastAPI**: 现代化的Web框架
- **Uvicorn**: ASGI服务器
- **PyMySQL**: MySQL数据库驱动
- **Pydantic**: 数据验证和序列化

## 项目结构

```
haiwailiuxue/
├── api/
│   ├── __init__.py
│   └── customer_api.py          # API接口定义
├── config/
│   ├── __init__.py
│   └── config.py                # 数据库配置
├── dao/
│   ├── __init__.py
│   └── database.py              # 数据访问层
├── service/
│   ├── __init__.py
│   └── customer_service.py      # 业务逻辑层
├── main.py                      # 主入口文件
├── requirements.txt             # 项目依赖
└── database_init.sql           # 数据库初始化脚本
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库配置

编辑 `config/config.py` 文件，修改数据库连接信息：

```python
DB_CONFIG = {
    'host': 'localhost',        # 数据库主机
    'port': 3306,              # 端口
    'user': 'root',            # 用户名
    'password': 'your_password',  # 密码
    'database': 'dify_customer',  # 数据库名
    'charset': 'utf8mb4'
}
```

### 3. 初始化数据库

执行 `database_init.sql` 脚本创建数据库和表：

```bash
mysql -u root -p < database_init.sql
```

或在MySQL客户端中执行：

```sql
source /path/to/database_init.sql;
```

### 4. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API接口说明

### 保存客户研判数据

**接口地址**: `POST /api/save_customer_judge`

**请求体示例**:

```json
{
  "name": "张三",
  "customer_age": 35,
  "customer_gender": "男",
  "customer_fund": "500万",
  "customer_address": "北京市朝阳区",
  "raw_data": "{\"key\": \"value\"}",
  "is_target": 1,
  "judge_reason": "符合目标客户标准，资金充足"
}
```

**字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 客户姓名 |
| customer_age | integer | 否 | 客户年龄 (0-120) |
| customer_gender | string | 否 | 客户性别 |
| customer_fund | string | 否 | 客户资金情况 |
| customer_address | string | 否 | 客户地址 |
| raw_data | string | 否 | 原始JSON数据 |
| is_target | integer | 否 | 客户类型：1=符合目标客户，2=潜在客户，0=非目标客户，3=信息不足 |
| judge_reason | string | 否 | 判断原因 |

**响应示例**:

成功响应:
```json
{
  "code": 200,
  "msg": "客户研判数据保存成功",
  "data": {
    "customer_id": 1
  }
}
```

失败响应:
```json
{
  "code": 500,
  "msg": "保存失败：错误详情",
  "data": null
}
```

### 健康检查

**接口地址**: `GET /` 或 `GET /health`

**响应示例**:
```json
{
  "code": 200,
  "msg": "服务运行正常",
  "data": {
    "service": "客户研判数据API",
    "status": "running"
  }
}
```

## Dify工作流配置

在Dify工作流的HTTP节点中配置：

1. **方法**: POST
2. **URL**: `http://your-server-ip:8000/api/save_customer_judge`
3. **Headers**: 
   - `Content-Type: application/json`
4. **Body**: 选择JSON格式，填入上述请求体

## 注意事项

1. `source` 字段固定值为 `client_judge`
2. `creator` 字段固定值为 `system`
3. `created_at` 和 `updated_at` 由数据库自动生成，无需传入
4. 生产环境建议关闭 `reload` 参数
5. 生产环境建议限制 `allow_origins` 为具体域名

## 常见问题

### Q: 如何修改服务端口？

A: 修改 `main.py` 中的 `port` 参数：

```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # 修改为8080端口
```

### Q: 如何启用热重载？

A: 将 `main.py` 中的 `reload` 参数改为 `True`：

```python
uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Q: 数据库连接失败怎么办？

A: 检查以下几点：
1. 数据库服务是否启动
2. `config/config.py` 中的配置是否正确
3. 网络是否通畅
4. 数据库用户是否有权限访问

## 许可证

MIT License
