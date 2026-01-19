from fastapi import APIRouter
from app.api.endpoints import emprunts

api_router = APIRouter()
api_router.include_router(emprunts.router, prefix="/emprunts")
