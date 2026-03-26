# Dify HTTP节点快速配置卡片

## 📋 快速配置

| 配置项 | 值 |
|--------|-----|
| **请求方法** | `POST` |
| **请求URL** | `http://your-server:8000/api/save_customer_judge` |
| **Body类型** | `JSON` |

## 🔧 请求头（Headers）

```json
{
  "Content-Type": "application/json",
  "Accept": "application/json"
}
```

## 📝 请求体（Body）

```json
{
  "name": "{{customer_name}}",
  "customer_age": {{customer_age}},
  "customer_gender": "{{customer_gender}}",
  "customer_fund": "{{customer_fund}}",
  "customer_address": "{{customer_address}}",
  "raw_data": "{{raw_data}}",
  "is_target": {{is_target}},
  "judge_reason": "{{judge_reason}}"
}
```

## 📊 字段说明

| 字段 | 类型 | 必填 | 说明 | Dify变量 |
|------|------|:----:|------|----------|
| `name` | string | ✅ | 客户姓名 | `{{name}}` |
| `customer_age` | integer | ❌ | 客户年龄 | `{{age}}` |
| `customer_gender` | string | ❌ | 客户性别 | `{{gender}}` |
| `customer_fund` | string | ❌ | 资金情况 | `{{fund}}` |
| `customer_address` | string | ❌ | 客户地址 | `{{address}}` |
| `raw_data` | string | ❌ | 原始数据 | `{{raw}}` |
| `is_target` | integer | ❌ | 客户类型 | `{{target}}` |
| `judge_reason` | string | ❌ | 判断原因 | `{{reason}}` |

## 🎯 is_target 枚举值

| 值 | 说明 |
|----|------|
| `1` | 符合目标客户 |
| `2` | 潜在客户 |
| `0` | 非目标客户 |
| `3` | 信息不足 |

## ✅ 成功响应

```json
{
  "code": 200,
  "msg": "客户研判数据保存成功",
  "data": {
    "customer_id": 1
  }
}
```

## ❌ 失败响应

```json
{
  "code": 500,
  "msg": "保存失败：错误详情",
  "data": null
}
```

## 🔗 响应数据引用

```javascript
// 状态码
{{http_response.code}}

// 消息
{{http_response.msg}}

// 客户ID
{{http_response.data.customer_id}}
```

## ⚙️ 条件判断示例

```javascript
// 判断是否成功
{{http_response.code}} == 200

// 获取客户ID
{{http_response.data.customer_id}}
```

---

**💡 提示**: 修改URL中的 `your-server` 为实际服务器地址  
**📖 完整文档**: 查看 `DIFY_HTTP_CONFIG.md`
