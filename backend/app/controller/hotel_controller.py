from fastapi import APIRouter, Depends, Response
from app.config.database_config import db_dependency
from app.entity.user_entity import User
from app.util.auth import get_current_user
from app.service.hotel_service import HotelService
from app.model.hotel_model import HotelCreate, HotelUpdate
from app.service.hotel_service import HotelService

hotel_router = APIRouter(
    prefix="/api/v1/hotels",
    tags=["Hotel"]
)

hotel_service = HotelService()

@hotel_router.get("/")
def get_hotels(
    response: Response,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Get all hotels.
    
    Returns a list of all hotels in the system.
    """
    res = hotel_service.get_all_hotels(db=db)
    response.status_code = res.status_code
    return res

@hotel_router.get("/{hotel_id}")
def get_hotel(
    response: Response,
    hotel_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Get hotel by ID.
    
    Returns detailed information about a specific hotel including room types.
    """
    res = hotel_service.get_hotel(db=db, hotel_id=hotel_id)
    response.status_code = res.status_code
    return res

@hotel_router.post("/")
def create_hotel(
    response: Response,
    hotel: HotelCreate,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Create a new hotel.
    
    Creates a hotel with the provided name, location, and description.
    """
    res =  hotel_service.create_hotel(db=db, hotel_data=hotel.dict())
    response.status_code = res.status_code
    return res
       
@hotel_router.put("/{hotel_id}")
def update_hotel(
    response: Response,
    hotel_id: int,
    hotel_update: HotelUpdate,
    db:db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Update an existing hotel.
    
    Updates hotel information. Only provided fields will be updated.
    """
    res = hotel_service.update_hotel(db=db, hotel_id=hotel_id, update_data=hotel_update.dict(exclude_unset=True))
    response.status_code = res.status_code
    return res

@hotel_router.delete("/{hotel_id}")
def delete_hotel(
    response: Response,
    hotel_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user)):
    
    """
    Delete a hotel.
    
    Permanently deletes a hotel and all associated room types.
    """
    res =  hotel_service.delete_hotel(db=db, hotel_id=hotel_id)
    response.status_code = res.status_code
    return res
