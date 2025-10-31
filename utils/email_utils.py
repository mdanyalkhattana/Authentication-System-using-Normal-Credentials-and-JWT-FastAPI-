import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import settings
from jinja2 import Environment, FileSystemLoader

def send_verification_email(to_email: str, verify_token: str):
    subject = "Verify your account"
    verify_link = f"http://127.0.0.1:8000/verify/email?token={verify_token}"

    body = f"""
    <h2>Verify Your Account</h2>
    <p>Click below to verify your email:</p>
    <a href="{verify_link}" target="_blank">Verify My Account</a>
    <br><br>
    <p>If you did not request this, please ignore this email.</p>
    """

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(msg)


def send_reset_password_email(to_email: str, reset_token: str):
    """Send email with reset password link using HTML template"""
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("reset_password_email.html")

    reset_link = f"http://127.0.0.1:8000/password/reset-form?token={reset_token}"
    html_content = template.render(reset_link=reset_link)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Your Password"
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(msg)
