from pydantic import BaseModel, Field
from datetime import datetime

class RateAdjustmentBase(BaseModel):
    adjustment_amount: float
    effective_date: datetime
    reason: str = Field(..., min_length=1)


class RateAdjustmentCreate(RateAdjustmentBase):
    room_type_id: int


class RateAdjustmentResponse(RateAdjustmentBase):
    id: int
    room_type_id: int
    created_at: datetime

    class Config:
        from_attributes = True