from fastapi import APIRouter
from pydantic import BaseModel
from typing import Protocol
from app.api.api_v1.endpoints.wadus import Storage, FileStorage
from app.schemas.topics import Topic

topics = [
    Topic(name="Sales", channel="slack"),
    Topic(name="Pricing", channel="email"),
]


router = APIRouter()


@router.get("/")
async def root():
    return topics
