import logging

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, Patients
from app.exceptions.configure_exceptions import (
    ItemDoesNotExist, BothEmailAndPhoneAreNone, ItemExist,
    ErrorRequestException
)
from app.schemas.users import CheckUserExistRequest
from app.common.password import PasswordHandler
from app.common.auth import create_user_token

logger = logging.getLogger("default")


async def login_process(
    user_id: int,
    user_password: str,
    req_password: str,
    is_admin: bool
):
    await PasswordHandler().verify_password(
        plain_password=req_password,
        hashed_password=user_password
    )
    access_token, refresh_token = await create_user_token(
        user_id=user_id,
        is_admin=is_admin
    )
    return access_token, refresh_token
