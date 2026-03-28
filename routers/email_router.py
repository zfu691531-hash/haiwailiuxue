"""邮件路由"""

from fastapi import APIRouter, HTTPException, status
from models.schemas import EmailRequest, APIResponse
from config.config import EMAIL_CONFIG
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter(prefix="/api/email", tags=["邮件服务"])


@router.post(
    "/send",
    response_model=APIResponse,
    summary="发送邮件",
    description="发送邮件，支持主送和抄送"
)
async def send_email(req: EmailRequest):
    """
    邮件发送接口

    Args:
        req: 邮件请求
        - to: 主送邮箱列表
        - cc: 抄送邮箱列表
        - subject: 邮件标题
        - content: 邮件正文
        - content_type: 内容格式，默认 text/markdown

    Returns:
        APIResponse: 发送结果

    Raises:
        HTTPException: 发送失败时返回错误
    """
    try:
        # 验证必要参数
        if not req.to and not req.cc:
            logger.warning("邮件发送失败：未提供收件人")
            raise ValueError("至少需要提供主送邮箱或抄送邮箱")

        if not req.subject or req.subject.strip() == "":
            logger.warning("邮件发送失败：邮件标题为空")
            raise ValueError("邮件标题不能为空")

        if not req.content or req.content.strip() == "":
            logger.warning("邮件发送失败：邮件正文为空")
            raise ValueError("邮件正文不能为空")

        logger.info(f"开始发送邮件：标题={req.subject}，主送={req.to}，抄送={req.cc}")

        # 创建邮件对象 - 使用标准 MIMEText
        msg = MIMEText(req.content, 'plain', 'utf-8')
        msg['From'] = Header(EMAIL_CONFIG['smtp_user'], 'utf-8')
        msg['Subject'] = Header(req.subject, 'utf-8')

        # 设置主送和抄送
        if req.to:
            msg['To'] = ', '.join(req.to)
        if req.cc:
            msg['Cc'] = ', '.join(req.cc)

        # 合并所有收件人
        all_recipients = []
        if req.to:
            all_recipients.extend(req.to)
        if req.cc:
            all_recipients.extend(req.cc)

        # 使用 with 语法确保 SMTP 连接自动释放，添加超时时间
        try:
            with smtplib.SMTP_SSL(
                EMAIL_CONFIG['smtp_server'],
                EMAIL_CONFIG['smtp_port'],
                timeout=30
            ) as smtp:
                logger.debug(f"连接SMTP服务器：{EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")

                # 登录
                smtp.login(EMAIL_CONFIG['smtp_user'], EMAIL_CONFIG['smtp_password'])
                logger.debug("SMTP登录成功")

                # 发送邮件
                smtp.sendmail(EMAIL_CONFIG['smtp_user'], all_recipients, msg.as_string())
                logger.info(f"邮件发送成功：收件人数量={len(all_recipients)}")

        except smtplib.SMTPAuthenticationError as auth_error:
            logger.error(f"SMTP认证失败：{str(auth_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='邮件发送失败：SMTP认证失败，请检查邮箱账号和密码'
            )
        except smtplib.SMTPException as smtp_error:
            logger.error(f"SMTP服务异常：{str(smtp_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'邮件发送失败：SMTP服务异常 - {str(smtp_error)}'
            )
        except Exception as smtp_unknown_error:
            logger.error(f"SMTP未知错误：{str(smtp_unknown_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'邮件发送失败：网络连接异常'
            )

        return APIResponse(
            code=200,
            msg='邮件发送成功',
            data={
                'to': req.to,
                'cc': req.cc,
                'subject': req.subject,
                'recipient_count': len(all_recipients)
            }
        )

    except ValueError as ve:
        # 参数验证错误（已记录日志）
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'参数验证失败：{str(ve)}'
        )
    except HTTPException:
        # 已处理的 HTTP 异常直接抛出
        raise
    except Exception as e:
        logger.error(f"邮件发送未知错误：{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'邮件发送失败：系统异常'
        )
