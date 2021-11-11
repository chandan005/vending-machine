from fastapi import APIRouter

from .users.routes import users_router
# from .zoom_meetings.routes import zoom_meetings_router
# from .connect_live.routes import connect_live_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
# router.include_router(zoom_meetings_router, prefix="/zoom_meetings", tags=["Meetings"])
# router.include_router(connect_live_router, prefix="/connect_live", tags=["Connect Live"])