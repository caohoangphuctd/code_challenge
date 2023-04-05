import logging
from typing import Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.common.common import message_format
from app.common.auth import depend_admin_access_token
from app.database.depends import create_session
from app.schemas import ApiResponse
from app.schemas.users import (
    CreateGroupRequest, CreateGroupResponse,
    AddPatientToGroupRequest
)

logger = logging.getLogger("default")

router = APIRouter(prefix="/groups", tags=["groups"])


CREATE_GROUP_STATUS_CODES = {201: {"description": "A group was created"}}
ADD_PATIENT_TO_GROUP_STATUS_CODES = {
    200: {"description": "A group was created"}
}


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
    group = await controllers.groups.create_group(db, schema)
    return await message_format(data=group)


@router.post(
    "/addPatientToGroup",
    response_model=ApiResponse,
    responses=ADD_PATIENT_TO_GROUP_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_200_OK,
)
async def add_patient_to_group(
    schema: AddPatientToGroupRequest,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    logger.info("Create user")
    await controllers.groups.add_patient_to_group(db, schema)
    return await message_format(message="Added")
