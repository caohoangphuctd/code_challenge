import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.common.common import message_format
from app.common.auth import depend_admin_access_token
from app.database.depends import create_session
from app.schemas import ApiResponse
from app.schemas.users import (
    CreateInfantOrChildRequest, CreateInfantOrChildResponse
)

logger = logging.getLogger("default")

router = APIRouter(prefix="/patients", tags=["patients"])


SEARCH_PATIENTS_STATUS_CODES = {200: {"description": "Search successfully"}}
GET_PATIENT_STATUS_CODES = {
    200: {"description": "Get patient by id"}
}
CREATE_GROUP_STATUS_CODES = {201: {"description": "A group was created"}}


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
    patient = await controllers.patients.create_infant_or_child(db, schema)
    return await message_format(data=patient)


@router.get(
    "",
    response_model=ApiResponse[List[CreateInfantOrChildResponse]],
    responses=SEARCH_PATIENTS_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_200_OK,
)
async def search_patients(
    search: str,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    data = await controllers.patients.search_patients(db, search)
    return await message_format(data=data)


@router.get(
    "/{patient_id}",
    response_model=ApiResponse[CreateInfantOrChildResponse],
    responses=GET_PATIENT_STATUS_CODES,  # type: ignore
    status_code=status.HTTP_200_OK,
)
async def get_patient_by_id(
    patient_id: int,
    db: AsyncSession = Depends(create_session),
    _authorize: Dict = Depends(depend_admin_access_token)
):
    data = await controllers.patients.get_patient_by_id(db, patient_id)
    return await message_format(data=data)
