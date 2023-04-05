import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Patients, Groups, PatientGroups
from app.exceptions.configure_exceptions import (
    ItemDoesNotExist
)
from app.schemas.users import (
    CreateGroupRequest, AddPatientToGroupRequest
)

logger = logging.getLogger("default")


async def create_group(
    db: AsyncSession,
    group_info: CreateGroupRequest
):
    group = Groups(**group_info.dict())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def add_patient_to_group(
    db: AsyncSession,
    schema: AddPatientToGroupRequest
):
    stmt = select(Patients).where(
        Patients.id == schema.patient_id
    )
    patient = await db.execute(stmt)
    patient: Patients = patient.scalar()
    if not patient:
        raise ItemDoesNotExist("PatientId")
    stmt = select(Groups).where(
        Groups.id == schema.group_id
    )
    group = await db.execute(stmt)
    group: Patients = patient.scalar()
    if not group:
        raise ItemDoesNotExist("GroupId")

    group = PatientGroups(**schema.dict())
    db.add(group)
    await db.commit()
    await db.refresh(group)
