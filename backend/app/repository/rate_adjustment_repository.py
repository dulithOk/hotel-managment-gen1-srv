from datetime import datetime
from sqlalchemy.orm import Session
from app.entity.rate_adjustment_entity import RateAdjustment

class RateAdjustmentRepository:

    @staticmethod
    def get_by_room_type(db: Session, room_type_id: int):
        return (
            db.query(RateAdjustment)
            .filter(RateAdjustment.room_type_id == room_type_id)
            .order_by(RateAdjustment.effective_date.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, adjustment_data: dict):
        adjustment = RateAdjustment(**adjustment_data)
        db.add(adjustment)
        db.commit()
        db.refresh(adjustment)
        return adjustment
    
    @staticmethod
    def get_latest_active_adjustment(db: Session, room_type_id: int):
        """Get the latest rate adjustment where effective_date <= now"""
        now = datetime.utcnow()
        return (
            db.query(RateAdjustment)
            .filter(
                RateAdjustment.room_type_id == room_type_id,
                RateAdjustment.effective_date <= now
            )
            .order_by(RateAdjustment.effective_date.desc())
            .first()
        )
        
rate_adjustment_repository = RateAdjustmentRepository()