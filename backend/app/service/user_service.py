from datetime import timedelta
from app.model.user_model import UserLogin
from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.config.config import settings
from app.model.generic_response import GenericResponse
from app.repository.user_repository import user_repository
from app.util.auth import create_access_token, verify_password
from app.exception.base_exception import BaseAppException

logger = get_logger(class_name=__name__)

class UserService:
    
    @classmethod
    def create_user(cls, user_login: UserLogin, db: db_dependency):
        try:
            logger.info("Starting User Creation")
            user = user_repository.get_user_by_username(db=db, username=user_login.username)
            if not user or not verify_password(user_login.password, user.hashed_password):
                return GenericResponse.failed(
                    message="Incorrect username or password",
                    results={},
                    status_code=401
                )
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
            )
            return GenericResponse.success(
                message="Login successful",
                results={"access_token": access_token, "token_type": "bearer"},
                status_code=200
            )
        except BaseAppException as e:
            logger.info(f"Create user failed: {e.message}")
            return GenericResponse.failed(message=f"Create role failed: {e.message}", results={}, status_code=e.status)
        except Exception as e:
            logger.error(f"Unexpected error in create user: {str(e)}")
            return GenericResponse.failed(message="Unable to create role", results={}, status_code=500)