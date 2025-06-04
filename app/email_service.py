from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from typing import List
from .configs.logging_config import logger

logger.critical(os.environ.get("AUTH_SERVICE_URL"))


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
            MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
            MAIL_FROM=os.environ.get("MAIL_FROM"),
            MAIL_PORT=587,
            MAIL_SERVER=os.environ.get("MAIL_SERVER", "smtp.gmail.com"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

        self.fm = FastMail(self.conf)

    async def send_verification_email(
        self, email: str, name: str, user_id: int, verification_token: str
    ):
        """Send email verification email"""
        auth_service_url = os.environ.get("AUTH_SERVICE_URL", "http://localhost:1000")
        verification_link = f"{auth_service_url}/auth/verify-email?user_id={user_id}&token={verification_token}"
        logger.critical(f"url: {auth_service_url}")
        html_content = f"""
        <html>
        <body>
            <h2>Welcome to Our Service, {name}!</h2>
            <p>Thank you for registering. Please click the link below to verify your email address:</p>
            <p><a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p>If you didn't create an account, please ignore this email.</p>
            <p>This link will expire in 24 hours.</p>
            <p><strong>Alternative:</strong> You can also verify using curl:</p>
            <code style="background-color: #f4f4f4; padding: 10px; display: block; margin: 10px 0;">
curl -X POST "{auth_service_url}/auth/verify-email"
  -H "Content-Type: application/json"
  -d '{{"user_id": {user_id}, "token": "{verification_token}"}}'
            </code>
        </body>
        </html>
        """
        message = MessageSchema(
            subject="Verify Your Email Address",
            recipients=[email],
            body=html_content,
            subtype="html",
        )
        await self.fm.send_message(message)
