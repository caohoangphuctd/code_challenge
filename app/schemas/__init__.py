from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

from app.schemas import users  # noqa: F401

DataType = TypeVar("DataType")


class ApiResponse(GenericModel, Generic[DataType]):
    message: Optional[str] = None
    data: Optional[DataType] = None
    status: bool = True
