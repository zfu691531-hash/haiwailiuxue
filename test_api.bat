@echo off
chcp 65001 >nul
echo ============================================================
echo 后端接口测试命令集 (Windows版本）
echo 所有接口都使用 http://localhost:8000 作为基础URL
echo ============================================================
echo.

REM ============================================================
REM 1. 健康检查接口
REM ============================================================
echo [测试1] 健康检查...
curl -X GET "http://localhost:8000/" -H "Content-Type: application/json"
echo.

REM ============================================================
REM 2. 创建日报接口
REM ============================================================
echo [测试2] 创建日报...
curl -X POST "http://localhost:8000/api/employee/report/create" -H "Content-Type: application/json" -d "{\"employee_id\": 1001, \"name\": \"2025-03-28工作日报\", \"report_date\": \"2025-03-28\", \"content\": \"完成日报查询功能优化，增加了部门、状态等查询参数\", \"achievements\": \"成功优化日报查询接口，支持更多查询条件\", \"plan_tomorrow\": \"继续优化其他接口功能\", \"problems\": \"暂无问题\", \"is_pushed\": 0}"
echo.

REM ============================================================
REM 3. 更新日报接口
REM ============================================================
echo [测试3] 更新日报...
curl -X POST "http://localhost:8000/api/employee/report/update" -H "Content-Type: application/json" -d "{\"id\": 1, \"employee_id\": 1001, \"name\": \"2025-03-28工作日报（已更新）\", \"report_date\": \"2025-03-28\", \"content\": \"完成日报查询功能优化，增加了部门、状态等查询参数，并进行了测试验证\", \"achievements\": \"成功优化日报查询接口，支持更多查询条件，已测试通过\", \"plan_tomorrow\": \"继续优化其他接口功能\", \"problems\": \"暂无问题\", \"status\": \"已提交\"}"
echo.

REM ============================================================
REM 4. 查询日报接口 - 查询所有
REM ============================================================
echo [测试4-1] 查询日报 - 查询所有...
curl -X POST "http://localhost:8000/api/employee/report/query" -H "Content-Type: application/json" -d "{}"
echo.

REM ============================================================
REM 5. 查询日报接口 - 按员工ID查询
REM ============================================================
echo [测试4-2] 查询日报 - 按员工ID查询...
curl -X POST "http://localhost:8000/api/employee/report/query" -H "Content-Type: application/json" -d "{\"employee_id\": 1001}"
echo.

REM ============================================================
REM 6. 查询日报接口 - 按部门查询
REM ============================================================
echo [测试4-3] 查询日报 - 按部门查询...
curl -X POST "http://localhost:8000/api/employee/report/query" -H "Content-Type: application/json" -d "{\"department_id\": 1}"
echo.

REM ============================================================
REM 7. 查询日报接口 - 按状态查询
REM ============================================================
echo [测试4-4] 查询日报 - 按状态查询...
curl -X POST "http://localhost:8000/api/employee/report/query" -H "Content-Type: application/json" -d "{\"status\": \"已提交\"}"
echo.

REM ============================================================
REM 8. 查询日报接口 - 按日期范围查询
REM ============================================================
echo [测试4-5] 查询日报 - 按日期范围查询...
curl -X POST "http://localhost:8000/api/employee/report/query" -H "Content-Type: application/json" -d "{\"start_date\": \"2025-03-01\", \"end_date\": \"2025-03-31\"}"
echo.

REM ============================================================
REM 9. 创建意向客户接口
REM ============================================================
echo [测试5] 创建意向客户...
curl -X POST "http://localhost:8000/api/employee/potential/customer/create" -H "Content-Type: application/json" -d "{\"customer_name\": \"张三\", \"customer_age\": 35, \"customer_gender\": \"男\", \"customer_address\": \"北京市朝阳区\", \"customer_fund\": \"500万\", \"intention_level\": \"高\", \"intention_product\": \"留学美国\", \"follow_employee_id\": 1001, \"status\": \"初接触\", \"source\": \"employee\", \"remark\": \"有强烈留学意向，资金充足\"}"
echo.

REM ============================================================
REM 10. 发送邮件接口 - 主送
REM ============================================================
echo [测试6-1] 发送邮件 - 主送...
curl -X POST "http://localhost:8000/api/email/send" -H "Content-Type: application/json" -d "{\"to\": [\"recipient@example.com\"], \"subject\": \"测试邮件\", \"content\": \"这是一封测试邮件，测试邮件发送功能是否正常工作。\", \"content_type\": \"text/markdown\"}"
echo.

REM ============================================================
REM 11. 发送邮件接口 - 含抄送
REM ============================================================
echo [测试6-2] 发送邮件 - 含抄送...
curl -X POST "http://localhost:8000/api/email/send" -H "Content-Type: application/json" -d "{\"to\": [\"test@example.com\"], \"cc\": [\"leader@example.com\"], \"subject\": \"日报通知\", \"content\": \"各位领导好，\\n\\n以下是今日的工作日报内容：\\n\\n# 主要工作\\n1. 完成了日报查询功能的优化\\n2. 增加了部门、状态等查询条件\\n\\n# 明日计划\\n继续优化其他接口功能\\n\\n谢谢！\", \"content_type\": \"text/markdown\"}"
echo.

REM ============================================================
REM 12. 客户研判接口
REM ============================================================
echo [测试7] 客户研判...
curl -X POST "http://localhost:8000/api/customer/judge" -H "Content-Type: application/json" -d "{\"name\": \"李四\", \"creator_id\": 1001, \"creator\": \"王经理\", \"customer_age\": 28, \"customer_gender\": \"女\", \"customer_fund\": \"100万\", \"customer_address\": \"上海市浦东新区\", \"source\": \"client_judge\", \"raw_data\": \"{\\\"age\\\": 28, \\\"gender\\\": \\\"女\\\", \\\"fund\\\": \\\"100万\\\"}\", \"is_target\": 2, \"judge_reason\": \"潜在客户，有发展空间，建议跟进\"}"
echo.

REM ============================================================
REM 13. SQL执行接口 - 查询员工表
REM ============================================================
echo [测试8-1] SQL执行 - 查询员工表...
curl -X POST "http://localhost:8000/api/execute_sql" -H "Content-Type: application/json" -d "{\"sql\": \"SELECT * FROM employee LIMIT 10\"}"
echo.

REM ============================================================
REM 14. SQL执行接口 - 按条件查询
REM ============================================================
echo [测试8-2] SQL执行 - 按条件查询...
curl -X POST "http://localhost:8000/api/execute_sql" -H "Content-Type: application/json" -d "{\"sql\": \"SELECT id, name, role, department_name FROM employee WHERE role = '普通员工' LIMIT 5\"}"
echo.

REM ============================================================
REM 15. SQL执行接口 - 查询日报表
REM ============================================================
echo [测试8-3] SQL执行 - 查询日报表...
curl -X POST "http://localhost:8000/api/execute_sql" -H "Content-Type: application/json" -d "{\"sql\": \"SELECT id, employee_id, report_date, status, created_at FROM daily_report ORDER BY report_date DESC LIMIT 10\"}"
echo.

REM ============================================================
REM 16. SQL执行接口 - 统计数据
REM ============================================================
echo [测试8-4] SQL执行 - 统计数据...
curl -X POST "http://localhost:8000/api/execute_sql" -H "Content-Type: application/json" -d "{\"sql\": \"SELECT status, COUNT(*) as count FROM daily_report GROUP BY status\"}"
echo.

echo ============================================================
echo 测试命令使用说明：
echo ============================================================
echo 1. 确保服务已启动: python main.py
echo 2. 双击运行此 test_api.bat 文件
echo 3. 或者单独复制某条命令到命令行执行
echo.
echo 提示：
echo - 将 localhost:8000 替换为 host.docker.internal:8000 可在 Docker 中访问
echo - 修改 JSON 数据中的 ID 和邮箱地址以适应您的环境
echo - 邮件发送前请确认邮箱配置正确
echo ============================================================
pause
