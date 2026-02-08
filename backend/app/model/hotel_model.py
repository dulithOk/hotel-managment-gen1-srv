from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class HotelBase(BaseModel):
    name: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    description: Optional[str] = None


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None


class HotelResponse(HotelBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True