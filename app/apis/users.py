import logging
from typing import Dict, List

from redis.asyncio import Redis
from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.common.common import message_format, get_random_otp
from app.common.handle_twilio import send_otp, send_password
from app.common.auth import depend_admin_access_token
from app.database.depends import create_session, get_redis_db
from app.schemas import ApiResponse
from app.schemas.users import (
    CheckUserExistRequest, CreateUserRequest, LoginRequest,
    CreateGroupRequest, CreateGroupResponse, CreateUserResponse,
    AddPatientToGroupRequest, CreateInfantOrChildRequest,
    CreateInfantOrChildResponse
)

logger = logging.getLogger("default")

router = APIRouter(prefix="/users", tags=["users"])


CREATE_USERS_STATUS_CODES = {201: {"description": "A user was created"}}
CHECK_USERS_EXIST_STATUS_CODES = {
    200: {"description": "Check email or phone number valid"}
}
LOGIN_STATUS_CODES = {200: {"description": "Login successfully"}}
CREATE_GROUP_STATUS_CODES = {201: {"description": "A group was created"}}


@router.post(
    "/login",
    response_model=ApiResponse,
    responses=LOGIN_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_200_OK,
)
async def login(
    schema: LoginRequest,
    db: AsyncSession = Depends(create_session)
):
    user = await controllers.users.get_user_by_username(db, schema.username)
    access_token, refresh_token = await controllers.auth.login_process(
        user_id=user.id,
        user_password=user.password,
        req_password=schema.password,
        is_admin=user.is_admin
    )
    return await message_format(
        data={"access_token": access_token, "refresh_token": refresh_token},
        message="LoginSuccessfully"
    )


@router.post(
    "/checkUserExist",
    response_model=ApiResponse,
    responses=CHECK_USERS_EXIST_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_200_OK,
)
async def check_user_exist(
    information: CheckUserExistRequest,
    background_task: BackgroundTasks,
    db: AsyncSession = Depends(create_session),
    redis: Redis = Depends(get_redis_db),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    logger.info("Check user exist")
    await controllers.users.check_user_exist(db, information)
    otp = await get_random_otp(6)
    if information.phone_number:
        await redis.set(
            f"{information.phone_number}/{otp}", information.json(), ex=720
        )
        background_task.add_task(
            send_otp, phone_number=information.phone_number, otp=otp
        )
        result = "SentOTPViaSMS"
    elif information.email:
        await redis.set(
            f"{information.email}/{otp}", information.json(), ex=720
        )
        result = "SentOTPViaEmail"
    return await message_format(message=result)


@router.post(
    "/createUser",
    response_model=ApiResponse[CreateUserResponse],
    responses=CREATE_USERS_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    schema: CreateUserRequest,
    background_task: BackgroundTasks,
    db: AsyncSession = Depends(create_session),
    redis: Redis = Depends(get_redis_db),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    logger.info("Create user")
    if schema.phone_number:
        user_info = await redis.get(
            f"{schema.phone_number}/{schema.otp}"
        )
        result = "SentPasswordViaSMS"
    elif schema.email:
        user_info = await redis.get(
            f"{schema.email}/{schema.otp}"
        )
        result = "SentPasswordViaEmail"
    user_info = CheckUserExistRequest.parse_raw(user_info)
    user, password = await controllers.users.create_user(db, user_info)
    if schema.phone_number:
        background_task.add_task(
            send_password, phone_number=schema.phone_number, password=password
        )
    elif schema.email:
        pass
    return await message_format(message=result, data=user)


@router.post(
    "/createInfantOrChild",
    response_model=ApiResponse[CreateInfantOrChildResponse],
    responses=CREATE_GROUP_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_infant_or_child(
    schema: CreateInfantOrChildRequest,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    patient = await controllers.users.create_infant_or_child(db, schema)
    return await message_format(data=patient)


@router.post(
    "/createGroup",
    response_model=ApiResponse[CreateGroupResponse],
    responses=CREATE_GROUP_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    schema: CreateGroupRequest,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    group = await controllers.users.create_group(db, schema)
    return await message_format(data=group)


@router.post(
    "/addGroup",
    response_model=ApiResponse,
    responses=CREATE_USERS_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_to_group(
    schema: AddPatientToGroupRequest,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    logger.info("Create user")
    await controllers.users.add_patient_to_group(db, schema)
    return await message_format(message="Added")


@router.get(
    "/patients",
    response_model=ApiResponse[List[CreateInfantOrChildResponse]],
    responses=CREATE_USERS_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def search_patients(
    search: str,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    data = await controllers.users.search_patients(db, search)
    return await message_format(data=data)


@router.get(
    "/patient/{patient_id}",
    response_model=ApiResponse[CreateInfantOrChildResponse],
    responses=CREATE_USERS_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_201_CREATED,
)
async def get_patient_by_id(
    patient_id: int,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    data = await controllers.users.get_patient_by_id(db, patient_id)
    return await message_format(data=data)
