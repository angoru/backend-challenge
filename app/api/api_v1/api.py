from fastapi import APIRouter

from .endpoints import message, topics

router = APIRouter()
router.include_router(message.router, prefix="/message", tags=["Message"])
router.include_router(topics.router, prefix="/topics", tags=["Topics"])
