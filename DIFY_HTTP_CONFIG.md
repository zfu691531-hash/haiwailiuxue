# Dify工作流HTTP节点配置指南

本文档详细说明如何在Dify工作流中配置HTTP节点，调用客户研判数据保存接口。

## 一、HTTP节点基础配置

### 1. 节点选择
在Dify工作流编辑器中，拖拽 `HTTP Request` 节点到画布中。

### 2. 节点基础设置

**节点名称**: 保存客户研判数据
**节点描述**: 将客户研判结果保存到MySQL数据库

---

## 二、请求配置

### 2.1 请求方法

```
POST
```

### 2.2 请求URL

**开发环境**:
```
http://localhost:8000/api/save_customer_judge
```

**生产环境**（请替换为实际服务器IP）:
```
http://your-server-ip:8000/api/save_customer_judge
```

**内网环境**:
```
http://192.168.x.x:8000/api/save_customer_judge
```

### 2.3 请求头（Headers）

在 `Headers` 区域添加以下配置：

| Key | Value | 说明 |
|-----|-------|------|
| Content-Type | application/json | 指定请求体为JSON格式 |
| Accept | application/json | 指定期望的响应格式 |

**配置示例**:
```json
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

### 2.4 请求体（Body）

**Body类型**: `JSON`

在 `Body` 区域选择 `JSON` 类型，然后填入以下JSON模板：

```json
{
  "name": "{{姓名变量}}",
  "customer_age": {{年龄变量}},
  "customer_gender": "{{性别变量}}",
  "customer_fund": "{{资金变量}}",
  "customer_address": "{{地址变量}}",
  "raw_data": "{{原始数据变量}}",
  "is_target": {{客户类型变量}},
  "judge_reason": "{{判断原因变量}}"
}
```

---

## 三、字段映射说明

### 3.1 请求体字段详解

| 字段名 | 类型 | 必填 | 说明 | Dify变量示例 |
|--------|------|------|------|-------------|
| `name` | string | ✅ 是 | 客户姓名 | `{{customer_name}}` |
| `customer_age` | integer | ❌ 否 | 客户年龄（0-120） | `{{customer_age}}` |
| `customer_gender` | string | ❌ 否 | 客户性别 | `{{customer_gender}}` |
| `customer_fund` | string | ❌ 否 | 客户资金情况 | `{{customer_fund}}` |
| `customer_address` | string | ❌ 否 | 客户地址 | `{{customer_address}}` |
| `raw_data` | string | ❌ 否 | 原始JSON数据 | `{{raw_json_data}}` |
| `is_target` | integer | ❌ 否 | 客户类型（0/1/2/3） | `{{is_target}}` |
| `judge_reason` | string | ❌ 否 | 判断原因 | `{{judge_reason}}` |

### 3.2 客户类型枚举说明

`is_target` 字段的可选值：

| 值 | 说明 | 使用场景 |
|----|------|---------|
| `1` | 符合目标客户 | 客户完全符合目标画像 |
| `2` | 潜在客户 | 客户有一定潜力，需要跟进 |
| `0` | 非目标客户 | 客户不符合基本要求 |
| `3` | 信息不足 | 信息不完整，无法判断 |

**Dify条件分支示例**:

```python
# 在Dify的Code节点中设置is_target
if score >= 90:
    is_target = 1  # 符合目标客户
elif score >= 70:
    is_target = 2  # 潜在客户
elif score < 50:
    is_target = 0  # 非目标客户
else:
    is_target = 3  # 信息不足
```

---

## 四、完整配置示例

### 4.1 场景一：完整信息录入

**请求体JSON**:
```json
{
  "name": "{{customer_name}}",
  "customer_age": {{customer_age}},
  "customer_gender": "{{customer_gender}}",
  "customer_fund": "{{customer_fund}}",
  "customer_address": "{{customer_address}}",
  "raw_data": "{{#llm_response#}}",
  "is_target": {{is_target_code}},
  "judge_reason": "{{#llm_judge_reason#}}"
}
```

### 4.2 场景二：仅保存必要信息

**请求体JSON**:
```json
{
  "name": "{{customer_name}}",
  "customer_age": 0,
  "customer_gender": "",
  "customer_fund": "",
  "customer_address": "",
  "raw_data": "{{#llm_full_response#}}",
  "is_target": 3,
  "judge_reason": "信息不足"
}
```

### 4.3 场景三：从LLM响应中提取信息

假设LLM输出格式如下：
```json
{
  "name": "张三",
  "age": 35,
  "gender": "男",
  "fund": "500万",
  "address": "北京市朝阳区",
  "judge_result": {
    "is_target": true,
    "reason": "符合目标客户标准"
  }
}
```

**在Dify中配置**:

1. 先用 `Code节点` 解析LLM响应：
```python
import json

# 获取LLM响应
response = {{#llm_output#}}

# 解析JSON
data = json.loads(response)

# 提取字段
name = data.get('name', '')
age = data.get('age', 0)
gender = data.get('gender', '')
fund = data.get('fund', '')
address = data.get('address', '')

# 处理客户类型
judge = data.get('judge_result', {})
if judge.get('is_target', False):
    is_target = 1
else:
    is_target = 0
judge_reason = judge.get('reason', '')

# 输出变量
{
    "name": name,
    "age": age,
    "gender": gender,
    "fund": fund,
    "address": address,
    "is_target": is_target,
    "judge_reason": judge_reason
}
```

2. 在HTTP节点中使用解析后的变量：
```json
{
  "name": "{{name}}",
  "customer_age": {{age}},
  "customer_gender": "{{gender}}",
  "customer_fund": "{{fund}}",
  "customer_address": "{{address}}",
  "raw_data": "{{#llm_output#}}",
  "is_target": {{is_target}},
  "judge_reason": "{{judge_reason}}"
}
```

---

## 五、响应处理配置

### 5.1 响应格式

**成功响应（code=200）**:
```json
{
  "code": 200,
  "msg": "客户研判数据保存成功",
  "data": {
    "customer_id": 1
  }
}
```

**失败响应（code=500）**:
```json
{
  "code": 500,
  "msg": "保存失败：错误详情",
  "data": null
}
```

### 5.2 在Dify中使用响应数据

在HTTP节点的后续节点中，可以通过以下方式引用响应数据：

```javascript
// 引用响应状态码
{{http_response.code}}

// 引用响应消息
{{http_response.msg}}

// 引用客户ID
{{http_response.data.customer_id}}
```

### 5.3 条件分支示例

在Dify的 `IF/ELSE` 节点中判断请求是否成功：

**条件**:
```javascript
{{http_response.code}} == 200
```

**True分支（成功）**:
- 输出："客户数据保存成功，ID：{{http_response.data.customer_id}}"
- 继续后续流程

**False分支（失败）**:
- 输出："保存失败：{{http_response.msg}}"
- 发送错误通知或重试

---

## 六、高级配置

### 6.1 超时设置

在HTTP节点中设置超时时间：

```
超时时间: 30秒
```

### 6.2 重试机制

配置失败重试：

```
最大重试次数: 3
重试间隔: 2000毫秒
```

### 6.3 错误处理

在HTTP节点后添加 `Error Handler` 节点：

```python
# 错误处理逻辑
error_message = {{http_error}}
# 发送告警通知
# 记录错误日志
```

---

## 七、测试与调试

### 7.1 测试数据

**测试用例1 - 完整信息**:
```json
{
  "name": "张三",
  "customer_age": 35,
  "customer_gender": "男",
  "customer_fund": "500万",
  "customer_address": "北京市朝阳区",
  "raw_data": "{\"test\": \"data\"}",
  "is_target": 1,
  "judge_reason": "符合目标客户标准，资金充足"
}
```

**测试用例2 - 最小信息**:
```json
{
  "name": "李四",
  "customer_age": 0,
  "customer_gender": "",
  "customer_fund": "",
  "customer_address": "",
  "raw_data": "",
  "is_target": 3,
  "judge_reason": ""
}
```

### 7.2 验证步骤

1. **检查连接**: 确保Dify能访问FastAPI服务
2. **检查格式**: 确认Content-Type为application/json
3. **检查变量**: 确认所有Dify变量都已正确映射
4. **查看日志**: 在Dify日志中查看请求和响应详情
5. **数据库验证**: 在MySQL中查询数据是否正确保存

---

## 八、常见问题

### Q1: 请求超时怎么办？

**A**: 检查以下几点：
- FastAPI服务是否正常运行
- 网络连接是否通畅
- 增加HTTP节点的超时时间
- 检查数据库连接是否正常

### Q2: 返回500错误？

**A**: 可能的原因：
- 数据库连接失败（检查config.py配置）
- 数据库表不存在（执行database_init.sql）
- 字段类型不匹配（检查数据格式）
- 数据库权限不足

### Q3: 变量未生效？

**A**: 确认：
- 变量名称拼写正确
- 变量在之前的节点中已定义
- 使用双花括号 `{{}}` 包裹变量名

### Q4: 中文乱码？

**A**: 确保请求头中包含：
```
Content-Type: application/json; charset=utf-8
```

---

## 九、完整工作流示例

### 9.1 工作流节点顺序

```
开始 → LLM节点 → Code节点（解析） → HTTP节点（保存数据） → IF/ELSE（判断结果） → 结束
```

### 9.2 节点配置速查表

| 节点 | 功能 | 输出变量 |
|------|------|---------|
| Start | 输入客户信息 | `customer_info` |
| LLM | 客户研判分析 | `llm_response` |
| Code | 解析JSON数据 | `name`, `age`, `gender`, `fund`, `address`, `is_target`, `judge_reason` |
| HTTP | 保存到数据库 | `http_response` |
| IF/ELSE | 判断保存结果 | `success` |
| End | 输出最终结果 | `final_result` |

---

## 十、快速配置检查清单

在配置完成后，请逐项检查：

- [ ] 请求方法设置为 `POST`
- [ ] URL地址正确，可以访问
- [ ] 请求头包含 `Content-Type: application/json`
- [ ] 请求体类型选择 `JSON`
- [ ] `name` 字段已映射（必填）
- [ ] `is_target` 字段值为 0/1/2/3
- [ ] 所有Dify变量使用 `{{}}` 包裹
- [ ] 设置了合理的超时时间
- [ ] 配置了错误处理机制
- [ ] 测试数据能够正常保存

---

## 联系支持

如遇到问题，请检查：
1. FastAPI服务日志
2. Dify工作流日志
3. MySQL数据库日志
4. 网络连接状态

**文档版本**: v1.0  
**更新日期**: 2026-03-26  
**适用版本**: Dify v0.6+, FastAPI v0.104+
