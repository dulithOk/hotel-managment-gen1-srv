from app.config.database_config import SessionLocal, engine
from app.config.base import *
from app.util.auth import get_password_hash
from datetime import datetime, timedelta

def seed_database():
    """Seed database with initial data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Database already seeded!")
            return
        
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@hotel.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin_user)
        
        # Create sample hotels
        hotel1 = Hotel(
            name="Grand Plaza Hotel",
            location="New York, NY",
            description="Luxury hotel in the heart of Manhattan"
        )
        hotel2 = Hotel(
            name="Beachside Resort",
            location="Miami, FL",
            description="Beautiful oceanfront resort with stunning views"
        )
        db.add(hotel1)
        db.add(hotel2)
        db.commit()
        
        # Create room types for hotel1
        deluxe_room = RoomType(
            hotel_id=hotel1.id,
            name="Deluxe Room",
            description="Spacious room with city view",
            base_rate=150.0
        )
        suite = RoomType(
            hotel_id=hotel1.id,
            name="Executive Suite",
            description="Luxurious suite with separate living area",
            base_rate=300.0
        )
        
        # Create room types for hotel2
        ocean_view = RoomType(
            hotel_id=hotel2.id,
            name="Ocean View Room",
            description="Room with beautiful ocean views",
            base_rate=200.0
        )
        
        db.add_all([deluxe_room, suite, ocean_view])
        db.commit()
        
        # Create sample rate adjustments
        adjustment1 = RateAdjustment(
            room_type_id=deluxe_room.id,
            adjustment_amount=20.0,
            effective_date=datetime.utcnow() - timedelta(days=30),
            reason="High season pricing"
        )
        adjustment2 = RateAdjustment(
            room_type_id=deluxe_room.id,
            adjustment_amount=50.0,
            effective_date=datetime.utcnow() - timedelta(days=5),
            reason="Holiday premium"
        )
        
        db.add_all([adjustment1, adjustment2])
        db.commit()
        
        print("Database seeded successfully!")
        print("Login credentials: username=admin, password=admin123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
