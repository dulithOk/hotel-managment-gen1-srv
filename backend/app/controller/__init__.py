from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.controller.user_controller import user_router as user
from app.controller.hotel_controller import hotel_router as hotel
from app.controller.room_type_controller import room_type_router as room_type
from app.controller.rate_adjustment_controller import rate_adjustment_router as rate_adjustment

all_routers = APIRouter()

all_routers.include_router(user)
all_routers.include_router(hotel)
all_routers.include_router(room_type)
all_routers.include_router(rate_adjustment)

@all_routers.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
        <head>
            <title>Hotel Management API Service</title>
        </head>
        <body>
            <h1>Welcome to Hotel Management API Service</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
