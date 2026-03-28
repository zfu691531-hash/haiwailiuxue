"""配置文件"""

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'dify_customer',
    'charset': 'utf8mb4'
}

# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER"),
    "smtp_port": int(os.getenv("SMTP_PORT")),
    "smtp_user": os.getenv("SMTP_EMAIL"),    # 必须是完整邮箱
    "smtp_password": os.getenv("SMTP_AUTH_CODE")  # 必须是授权码
}
