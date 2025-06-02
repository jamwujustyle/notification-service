import httpx
import os
from .email_service import EmailService
from .configs.logging_config import logger

email_service = EmailService()


async def handle_user_registered_event(event_data: dict):
    """Handle user registration event by sending verification email"""
    try:
        user_id = event_data["user_id"]
        email = event_data["email"]
        name = event_data["name"]

        auth_service_url = os.environ.get("AUTH_SERVICE_URL", "http://localhost:1000")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{auth_service_url}/internal/verification-token/{user_id}"
            )

            if response.status_code == 200:
                token_data = response.json()
                verification_token = token_data["token"]

                await email_service.send_verification_email(
                    email=email,
                    name=name,
                    user_id=user_id,
                    verification_token=verification_token,
                )
                logger.debug(f"Verification email sent to {email}")
            else:
                logger.debug(f"Failed to get verification token for user {user_id}")
    except Exception as ex:
        logger.debug(f"Error handling user registered event: {ex}")
