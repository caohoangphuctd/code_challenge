import logging

from twilio.rest import Client

from app.config import config

account_sid = config.twilio_config.account_sid
auth_token = config.twilio_config.auth_token
client = Client(account_sid, auth_token)

logger = logging.getLogger("default")


async def send_otp(phone_number: str, otp: str):
    try:
        client.messages.create(
            messaging_service_sid='MG7ab7dce689d84f307740de31ba061291',
            to=phone_number,
            body=f'your OTP is {otp}'
        )
    except Exception as e:
        logger.error(e.__str__())


async def send_password(phone_number: str, password: str):
    try:
        client.messages.create(
            messaging_service_sid='MG7ab7dce689d84f307740de31ba061291',
            to=phone_number,
            body=f'Your password is {password}'
        )
    except Exception as e:
        logger.error(e.__str__())
