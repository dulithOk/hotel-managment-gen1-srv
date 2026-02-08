from fastapi import APIRouter, Response
from app.model.user_model import UserLogin
from app.config.database_config import db_dependency
from app.service.user_service import UserService


user_router = APIRouter(
    prefix="/api/v1/user",
    tags=["User"]
)
user_service = UserService()

@user_router.post("/login")
def login(response: Response, user_login: UserLogin, db: db_dependency):
    """Authenticate user and return JWT token"""
    res = user_service.create_user(user_login=user_login, db=db)
    response.status_code = res.status_code
    return res
