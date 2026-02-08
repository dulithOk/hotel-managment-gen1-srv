from fastapi import APIRouter, Response, Depends
from app.config.database_config import db_dependency
from app.service.rate_adjustment_service import RateAdjustmentService
from app.entity.user_entity import User
from app.util.auth import get_current_user
from app.model.rate_adjustment_model import RateAdjustmentCreate

rate_adjustment_router = APIRouter(
    prefix="/api/v1/rate-adjustments",
    tags=["Rate Adjustment"]
)

rate_adjustment_service = RateAdjustmentService()
@rate_adjustment_router.get("/")
def get_rate_adjustments(
    response: Response,
    room_type_id: int,
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):  
    
    """
    Get rate adjustment history for a room type.
    
    Returns all rate adjustments for a specific room type, ordered by effective date.
    """
    res = rate_adjustment_service.get_rate_adjustments(
        db=db,
        room_type_id=room_type_id
    )
    response.status_code = res.status_code
    return res


@rate_adjustment_router.post("/")
def create_rate_adjustment(
    response: Response,
    adjustment: RateAdjustmentCreate,
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):  
    """
    Create a new rate adjustment.
    
    Records a rate adjustment for a room type with effective date and reason.
    The adjustment amount will be applied to calculate the effective rate.
    """
    res = rate_adjustment_service.create_rate_adjustment(
        db=db,
        adjustment_data=adjustment.dict()
    )
    response.status_code = res.status_code
    return res
