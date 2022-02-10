from fastapi import APIRouter

from .routers import citadel

router = APIRouter()
router.include_router(citadel.router, prefix="/citadel", tags=["Citadel"])