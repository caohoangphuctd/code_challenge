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
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)
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
    patientgroup_patient = relationship(    # type: ignore
        "PatientGroups", back_populates="patient"
    )


class Groups(BaseMixin, BaseModel):  # type: ignore
    id = Column(
        Integer, nullable=False, primary_key=True,
        autoincrement=True, index=True
    )
    group_name = Column(String(length=255), nullable=False)
    patientgroup_group = relationship(    # type: ignore
        "PatientGroups", back_populates="group"
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)


class PatientGroups(BaseMixin, BaseModel):  # type: ignore
    id = Column(
        Integer, nullable=False, primary_key=True,
        autoincrement=True, index=True
    )
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship(  # type: ignore
        "Groups", back_populates="patientgroup_group", cascade="all,delete"
    )
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    patient = relationship(  # type: ignore
        "Patients", back_populates="patientgroup_patient", cascade="all,delete"
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True)
