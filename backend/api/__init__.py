from fastapi import APIRouter

from api.routers.profile import profile_router 

main_router = APIRouter()


main_router.include_router(profile_router, prefix="/api")