from app.config.database_config import db_dependency
from app.entity.room_type_entity import RoomType
from app.repository.rate_adjustment_repository import rate_adjustment_repository

def calculate_effective_rate(room_type: RoomType, db: db_dependency) -> float:
    """
    Calculate effective rate based on the rule:
    effective_rate = base_rate + latest_adjustment_amount (where effective_date <= now)
    """    
    latest_adjustment = rate_adjustment_repository.get_latest_active_adjustment(
        db=db, 
        room_type_id=room_type.id
    )
    
    if latest_adjustment:
        return room_type.base_rate + latest_adjustment.adjustment_amount
    
    return room_type.base_rate