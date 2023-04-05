import logging

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, Patients, Groups, PatientGroups
from app.exceptions.configure_exceptions import (
    ItemDoesNotExist, BothEmailAndPhoneAreNone, ItemExist,
    ErrorRequestException
)
from app.schemas.users import (
    CheckUserExistRequest, CreateGroupRequest,
    AddPatientToGroupRequest, CreateInfantOrChildRequest
)
from app.common.password import PasswordHandler
from app.common.common import get_random_otp

logger = logging.getLogger("default")


async def get_user_by_username(
    db: AsyncSession,
    username: str
):
    stmt = select(Users).where(
        Users.username == username
    )
    user = await db.execute(stmt)
    user = user.scalar()
    if not user:
        raise ItemDoesNotExist("User")
    return user


async def check_user_exist(
    db: AsyncSession,
    user_info: CheckUserExistRequest,
):
    """Check user exist

    Args:
        db (AsyncSession): database session
        user_info (CheckUserExistRequest): input data
    """
    if not user_info.email and not user_info.phone_number:
        raise BothEmailAndPhoneAreNone()

    condition = []
    if user_info.email is not None:
        condition.append(
            Patients.email == user_info.email
        )
    if user_info.phone_number is not None:
        condition.append(
            Patients.phone_number == user_info.phone_number
        )
    if user_info.id_number is not None:
        condition.append(
            Patients.id_number == user_info.id_number
        )

    patient_stmt = select(Patients).where(
        or_(*condition)
    )
    patient = await db.execute(patient_stmt)
    patient: Patients = patient.scalar()
    if patient:
        if not user_info.email \
           and user_info.email == patient.email:
            raise ItemExist(field="Email")
        if not user_info.phone_number \
           and user_info.phone_number == patient.phone_number:
            raise ItemExist(field="PhoneNumber")
        if not user_info.id_number \
           and user_info.id_number == patient.id_number:
            raise ItemExist(field="IdNumber")


async def create_user(
    db: AsyncSession,
    user_info: CheckUserExistRequest,
):

    patient = Patients(**user_info.dict())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    password = await get_random_otp(8)
    password_hash = PasswordHandler().get_password_hash(password)
    if user_info.email:
        user = Users(
            username=user_info.email,
            password=password_hash,
            patient_id=patient.id
        )
    elif user_info.phone_number:
        user = Users(
            username=user_info.phone_number,
            password=password_hash,
            patient_id=patient.id
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return patient, password


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


async def create_group(
    db: AsyncSession,
    group_info: CreateGroupRequest
):
    group = Groups(**group_info.dict())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


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
