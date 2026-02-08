from sqlalchemy.orm import Session
from app.entity.hotel_entity import Hotel

class HotelRepository:

    @staticmethod
    def get_all_hotels(db: Session):
        return db.query(Hotel).all()

    @staticmethod
    def get_hotel_by_id(db: Session, hotel_id: int):
        return db.query(Hotel).filter(Hotel.id == hotel_id).first()

    @staticmethod
    def create_hotel(db: Session, hotel_data: dict):
        db_hotel = Hotel(**hotel_data)
        db.add(db_hotel)
        db.commit()
        db.refresh(db_hotel)
        return db_hotel

    @staticmethod
    def update_hotel(db: Session, db_hotel: Hotel, update_data: dict):
        for field, value in update_data.items():
            setattr(db_hotel, field, value)
        db.commit()
        db.refresh(db_hotel)
        return db_hotel

    @staticmethod
    def delete_hotel(db: Session, db_hotel: Hotel):
        db.delete(db_hotel)
        db.commit()


hotel_repository = HotelRepository()