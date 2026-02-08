from sqlalchemy.orm import Session
from app.entity.user_entity import User

class UserRepository:
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()


user_repository = UserRepository()