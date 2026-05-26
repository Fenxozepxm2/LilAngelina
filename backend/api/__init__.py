from fastapi import APIRouter

from api.routers.profile import profile_router
from api.routers.main_page import main_page_router
from api.routers.orders_page import orders_page_router
main_router = APIRouter()


main_router.include_router(profile_router, prefix="/api")
main_router.include_router(main_page_router)
main_router.include_router(orders_page_router)