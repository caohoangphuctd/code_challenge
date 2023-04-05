import logging

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Patients
from app.exceptions.configure_exceptions import (
    ItemDoesNotExist
)
from app.schemas.users import (
    CreateInfantOrChildRequest
)

logger = logging.getLogger("default")


async def create_infant_or_child(
    db: AsyncSession,
    info: CreateInfantOrChildRequest
):
    stmt = select(Patients).where(
        Patients.id == info.parent_id
    )
    patient = await db.execute(stmt)
    patient: Patients = patient.scalar()
    if not patient:
        raise ItemDoesNotExist("ParentId")
    patient = Patients(**info.dict())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient


async def search_patients(
    db: AsyncSession,
    search: str
):
    stmt = select(Patients).filter(
        or_(
            Patients.first_name.ilike(f"%{search}%"),
            Patients.last_name.ilike(f"%{search}%"),
            func.concat(
                Patients.first_name, " ", Patients.last_name
            ).ilike(f"%{search}%")
        )
    )
    patient = await db.execute(stmt)
    return patient.scalars().all()


async def get_patient_by_id(
    db: AsyncSession,
    patient_id: int
):
    stmt = select(Patients).where(
        Patients.id == patient_id
    )
    patient = await db.execute(stmt)
    patient: Patients = patient.scalar()
    if not patient:
        raise ItemDoesNotExist("PatientId")
    return patient
