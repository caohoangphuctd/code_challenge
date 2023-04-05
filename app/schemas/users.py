import re
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, validator, root_validator
from app.exceptions.configure_exceptions import BothEmailAndPhoneAreNone


class LoginRequest(BaseModel):
    username: str
    password: str


class CheckUserExistRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    id_number: str
    birth_date: date
    first_name: str
    last_name: str

    @validator("phone_number")
    def phone_validation(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

    class Config:
        orm_mode = True
        use_enum_values = True


class CreateUserResponse(CheckUserExistRequest):
    id: int
    created_at: datetime


class CreateUserRequest(BaseModel):
    otp: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @root_validator
    def validate_all(cls, values):
        if not values.get("phone_number") and not values.get("email"):
            raise BothEmailAndPhoneAreNone()
        return values


class CreateGroupRequest(BaseModel):
    group_name: str


class CreateGroupResponse(CreateGroupRequest):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AddPatientToGroupRequest(BaseModel):
    patient_id: int
    group_id: int


class CreateInfantOrChildRequest(CheckUserExistRequest):
    first_name: Optional[str] = None    # type: ignore
    last_name: Optional[str] = None     # type: ignore
    parent_id: Optional[int]


class CreateInfantOrChildResponse(CreateInfantOrChildRequest):
    id: int
    created_at: datetime
