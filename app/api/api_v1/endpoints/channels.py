from fastapi import APIRouter
from app.schemas.channels import Channel


channels = [
    Channel(name="Sales", plugin_class="Slack"),
    Channel(name="Pricing", plugin_class="Email"),
]

router = APIRouter()


@router.get("/")
async def root():
    return channels
