from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from dtos.position_dto import PositionDto


class EmployeeDto(BaseModel):
    id: str
    name: str
    last_name: str
    email: str
    position: PositionDto
    salary: float
    admission_date: datetime
    deleted: bool
    deleted_at: Optional[datetime]


class EmployeeFindAll(BaseModel):
    total: int
    pages: int
    employees: List[EmployeeDto]


class EmployeeCreate(BaseModel):
    name: str
    last_name: str
    email: str
    position: str
    salary: float
    admission_date: datetime

    def sanitize(self):
        self.name = self.name.strip().lower()
        self.last_name = self.last_name.strip().lower()
        self.email = self.email.strip().lower()

        return self


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    admission_date: Optional[datetime] = None

    def sanitize(self):
        self.name = self.name.strip().lower() if self.name else None
        self.last_name = self.last_name.strip().lower() if self.last_name else None
        self.email = self.email.strip().lower() if self.email else None

        return self
