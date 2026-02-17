from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.plants import router as plants_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(plants_router)
