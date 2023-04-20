from fastapi import APIRouter
from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    channel: str


topics = [
    Topic(name="Sales", channel="slack"),
    Topic(name="Pricing", channel="email"),
]

router = APIRouter()


@router.get("/")
async def root():
    return topics
