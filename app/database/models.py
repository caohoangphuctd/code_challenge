from datetime import datetime

from sqlalchemy import (
    Column, DateTime, Date, ForeignKey, Integer, String, Boolean
)
from sqlalchemy.orm import relationship

from app.database.config import BaseMixin, BaseModel


class Users(BaseMixin, BaseModel):  # type: ignore
    id = Column(
        Integer, nullable=False, primary_key=True,
        autoincrement=True, index=True
    )
    is_admin = Column(Boolean, nullable=False, default=False)
    username = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    patient = relationship(  # type: ignore
        "Patients", back_populates="user_patient", cascade="all,delete"
    )
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, nullable=True)


class Patients(BaseMixin, BaseModel):  # type: ignore
    id = Column(
        Integer, nullable=False, primary_key=True,
        autoincrement=True, index=True
    )
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    birth_date = Column(Date, nullable=False)
    id_number = Column(String(length=255), nullable=True)
    email = Column(String(length=255), nullable=True)
    phone_number = Column(String(length=255), nullable=True)
    parent_id = Column(Integer, ForeignKey("patients.id"))
    parent = relationship(  # type: ignore
        "Patients", backref="parent_obj", remote_side=[id],
        foreign_keys=[parent_id]
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)
    user_patient = relationship(    # type: ignore
        "Users", back_populates="patient"
    )
