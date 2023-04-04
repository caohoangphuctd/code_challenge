import re
from typing import Optional
from datetime import date
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


class CreateUserRequest(BaseModel):
    otp: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    @root_validator
    def validate_all(cls, values):
        if not values.get("phone_number") and not values.get("email"):
            raise BothEmailAndPhoneAreNone()
        return values
