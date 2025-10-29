import logging
from email.message import EmailMessage
from typing import Optional, Tuple
from config.config import settings
import aiosmtplib
from datetime import timedelta
from utils.token import create_access_token

logger = logging.getLogger("email_sender")


def _get_smtp_config() -> Tuple[Optional[str], Optional[int], Optional[str], Optional[str]]:
    server = getattr(settings, "SMTP_SERVER", None)
    port = getattr(settings, "SMTP_PORT", None)
    username = getattr(settings, "SMTP_EMAIL", None)
    password = getattr(settings, "SMTP_PASSWORD", None)
    return server, port, username, password


async def _send_smtp_message_async(msg: EmailMessage) -> None:
    server, port, username, password = _get_smtp_config()

    if not all([server, port, username, password]):
        # Missing SMTP configuration — fallback to logging the message for dev
        logger.warning("SMTP config missing, printing message instead")
        logger.info(msg)
        return

    # aiosmtplib.send will handle TLS/starttls depending on parameters
    try:
        if port == 465:
            await aiosmtplib.send(
                msg,
                hostname=server,
                port=port,
                username=username,
                password=password,
                use_tls=True,
            )
        else:
            await aiosmtplib.send(
                msg,
                hostname=server,
                port=port,
                username=username,
                password=password,
                start_tls=True,
            )
    except Exception as e:
        logger.exception("Failed to send email via SMTP: %s", e)
        raise


async def send_verification_email(to_email: str = None, reset_password_email: str = None) -> bool:
    """Send verification email with a secure token link."""
    if to_email is None and reset_password_email is None:
        return False

    email = to_email or reset_password_email

    # ✅ Step 1: Create a short-lived JWT token (10 mins expiry)
    token = create_access_token(
        data={"sub": email}
            )

    # ✅ Step 2: Create a verification link with token
    verification_link = f"http://127.0.0.1:8000/verify/verify-email?token={token}"

    # ✅ Step 3: Build email content
    subject = "Verify your email address"
    text = f"Please verify your email by clicking the link below:\n{verification_link}"
    html = f"""
        <html>
        <body>
            <p>Click below to verify your email:</p>
            <p><a href="{verification_link}" style="color: blue; text-decoration: underline;">Verify Email</a></p>
            <p>This link will expire in 10 minutes.</p>
        </body>
        </html>
    """

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_EMAIL or "no-reply@example.com"
    msg["To"] = email
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    # ✅ Step 4: Send email
    try:
        await _send_smtp_message_async(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

#  async def send_password_reset_email(to_email: str, reset_link: str) -> bool:
#     subject = "Password reset request"
#     text = f"Click the link to reset your password: {reset_link}\n\nIf you did not request this, ignore this email."
#     html = f"<p>Click to reset your password: <a href=\"{reset_link}\">Reset password</a></p>"

#     msg = EmailMessage()
#     msg["Subject"] = subject
#     msg["From"] = settings.SMTP_EMAIL or "no-reply@example.com"
#     msg["To"] = to_email
#     msg.set_content(text)
#     msg.add_alternative(html, subtype="html")

#     try:
#         await _send_smtp_message_async(msg)
#         return True
#     except Exception:
#         return False
