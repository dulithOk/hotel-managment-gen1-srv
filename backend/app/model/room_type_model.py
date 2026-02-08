from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RoomTypeBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    base_rate: float = Field(..., gt=0)


class RoomTypeCreate(RoomTypeBase):
    hotel_id: int


class RoomTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    base_rate: Optional[float] = Field(None, gt=0)


class RoomTypeResponse(RoomTypeBase):
    id: int
    hotel_id: int
    created_at: datetime
    effective_rate: float  # Calculated field

    class Config:
        from_attributes = True
        
