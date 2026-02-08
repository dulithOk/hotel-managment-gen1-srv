from sqlalchemy.orm import Session
from app.entity.room_type_entity import RoomType

class RoomTypeRepository:

    @staticmethod
    def get_all(db: Session, hotel_id: int = None):
        query = db.query(RoomType)
        if hotel_id:
            query = query.filter(RoomType.hotel_id == hotel_id)
        return query.all()

    @staticmethod
    def get_by_id(db: Session, room_type_id: int):
        return db.query(RoomType).filter(RoomType.id == room_type_id).first()

    @staticmethod
    def create(db: Session, room_type_data: dict):
        db_room_type = RoomType(**room_type_data)
        db.add(db_room_type)
        db.commit()
        db.refresh(db_room_type)
        return db_room_type

    @staticmethod
    def update(db: Session, db_room_type: RoomType, update_data: dict):
        for field, value in update_data.items():
            setattr(db_room_type, field, value)
        db.commit()
        db.refresh(db_room_type)
        return db_room_type

    @staticmethod
    def delete(db: Session, db_room_type: RoomType):
        db.delete(db_room_type)
        db.commit()


room_type_repository = RoomTypeRepository()