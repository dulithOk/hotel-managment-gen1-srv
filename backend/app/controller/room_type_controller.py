from fastapi import APIRouter, Depends, Response
from app.config.database_config import db_dependency
from app.config.database_config import db_dependency
from app.service.room_type_service import RoomTypeService
from app.entity.user_entity import User
from app.util.auth import get_current_user
from app.model.room_type_model import RoomTypeCreate, RoomTypeUpdate

room_type_router = APIRouter(
    prefix="/api/v1/room-types",
    tags=["Room Type"]
)

room_type_service = RoomTypeService()

@room_type_router.get("/")
def get_room_types(
    response: Response,
    db: db_dependency,
    hotel_id: int = None,
    current_user: User = Depends(get_current_user)):
    
    """
    Get all room types.
    
    Returns a list of all room types, optionally filtered by hotel.
    Query parameter hotel_id can be used to filter room types for a specific hotel.
    """
    res = room_type_service.get_all_room_types(db=db, hotel_id=hotel_id)
    response.status_code = res.status_code
    return res

@room_type_router.get("/{room_type_id}")
def get_room_type(
    response: Response,
    room_type_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Get room type by ID.
    
    Returns detailed information about a specific room type including effective rate.
    """
    res = room_type_service.get_room_type(db=db, room_type_id=room_type_id)
    response.status_code = res.status_code
    return res

@room_type_router.post("/")
def create_room_type(
    response: Response,
    room_type: RoomTypeCreate,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Create a new room type.
    
    Creates a room type with the provide name, description, base rate, and associated hotel.
    """
    res = room_type_service.create_room_type(db=db, room_type_data=room_type.dict())
    response.status_code = res.status_code
    return res

@room_type_router.put("/{room_type_id}")
def update_room_type(
    response: Response,
    room_type_id: int,
    room_type_update: RoomTypeUpdate,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Update an existing room type.
    
    Updates room type information. Only provided fields will be updated.
    """
    res = room_type_service.update_room_type(db=db, room_type_id=room_type_id, update_data=room_type_update.dict(exclude_unset=True))
    response.status_code = res.status_code
    return res

@room_type_router.delete("/{room_type_id}")
def delete_room_type(
    response: Response,
    room_type_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Delete a room type.
    
    Permanently deletes a room type and all associated rate adjustments.
    """
    res = room_type_service.delete_room_type(db=db, room_type_id=room_type_id)
    response.status_code = res.status_code
    return res
