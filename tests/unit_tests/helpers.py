import json
from pathlib import Path
from typing import Dict, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers, schemas
from app.database.models import Patients, Users

PATH_DATA_ROOT = Path(__file__).parent / "data"


def load_data(path: str) -> Dict:
    with open(PATH_DATA_ROOT / path) as f:
        return json.load(f)


async def create_records(
    session: AsyncSession, path: str
) -> Tuple[List[Patients], List[Users]]:
    patients = []
    users = []

    data = load_data(path)
    for patient in data["patients"]:
        obj = schemas.users.CheckUserExistRequest.parse_obj(patient)
        patient_record = Patients(**obj.dict())
        session.add(patient_record)
        await session.commit()
        await session.refresh(patient_record)
        patients.append(patient_record)

    for user in data["users"]:
        user_record = Users(**user)
        session.add(user_record)
        await session.commit()
        await session.refresh(user_record)
        users.append(user_record)

    return patients, users  # type: ignore
