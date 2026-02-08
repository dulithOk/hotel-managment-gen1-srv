from typing import List
from backend.app.model.hotel_model import HotelResponse
from backend.app.model.room_type_model import RoomTypeResponse


class HotelDetailResponse(HotelResponse):
    room_types: List[RoomTypeResponse] = []

    class Config:
        from_attributes = True
