from fastapi import APIRouter
from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    channel: str


channels = [
    Channel(name="slack", plugin_class="SlackPlugin"),
    Channel(name="email", plugin_class="EmailPlugin"),
]

router = APIRouter()


@router.get("/")
async def root():
    return channels
