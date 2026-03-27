from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 创建路由
router = APIRouter(prefix="/api/email", tags=["邮件服务"])


class EmailRequest(BaseModel):
    to: List[str] = []           # 主送邮箱
    cc: List[str] = []           # 抄送邮箱（领导填这里！）
    subject: str                 # 邮件标题
    content: str                 # 报告正文（Markdown）
    content_type: str = "text/markdown"  # 内容格式


@router.post("/send")
async def send_email(req: EmailRequest):
    try:
        result = send_email(req.to, req.cc, req.subject, req.content, req.content_type)

        return {
            "code": 200,
            "msg": "邮件发送成功，已抄送领导邮箱",
            "data": {
                "to": req.to,
                "cc": req.cc,
                "subject": req.subject
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"邮件发送失败：{str(e)}")
