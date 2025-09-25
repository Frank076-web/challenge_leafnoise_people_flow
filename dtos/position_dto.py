from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class PositionDto(BaseModel):
    id: str
    name: str
    deleted: bool
    deleted_at: Optional[datetime] = None


class FindAllPositionsDto(BaseModel):
    total: int
    pages: int
    positions: List[PositionDto]


class PositionCreate(BaseModel):
    name: str

    def sanitize(self):
        self.name = self.name.strip().lower()
        return self


class PositionUpdate(BaseModel):
    name: Optional[str] = None

    def sanitize(self):
        self.name = self.name.strip().lower() if self.name else None
        return self
