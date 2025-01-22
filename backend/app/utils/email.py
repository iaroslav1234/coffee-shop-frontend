import os
from typing import List
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, select_autoescape

# Initialize Jinja2 environment
env = Environment(
    loader=PackageLoader('app', 'templates/email'),
    autoescape=select_autoescape(['html', 'xml'])
)

async def send_email(
    to_email: str,
    subject: str,
    template_name: str,
    template_data: dict = None
) -> None:
    """
    Send an email using the specified template and data.
    """
    # Get email configuration from environment variables
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_username)

    if not all([smtp_host, smtp_port, smtp_username, smtp_password]):
        raise ValueError("Missing email configuration. Please check your environment variables.")

    # Create message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    # Render template
    template = env.get_template(f'{template_name}.html')
    html_content = template.render(**(template_data or {}))
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # Send email
    try:
        smtp = SMTP(hostname=smtp_host, port=smtp_port, use_tls=True)
        await smtp.connect()
        await smtp.login(smtp_username, smtp_password)
        await smtp.send_message(message)
        await smtp.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

async def send_password_reset_email(to_email: str, reset_token: str) -> None:
    """
    Send a password reset email to the user.
    """
    reset_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}"
    
    await send_email(
        to_email=to_email,
        subject="Reset Your Password - Coffee Shop Manager",
        template_name="password_reset",
        template_data={
            "reset_url": reset_url,
            "support_email": os.getenv('SUPPORT_EMAIL', 'support@coffeeshop.com')
        }
    )
