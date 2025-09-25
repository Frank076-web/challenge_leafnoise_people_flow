from typing import Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse[T](BaseModel):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    type_error: Optional[str] = None
