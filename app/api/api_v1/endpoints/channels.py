from fastapi import APIRouter
from app.schemas.channels import Channel
from app.models import Channels, Channel_Pydantic, ChannelIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

channels = [
    Channel(name="Sales", plugin_class="Slack"),
    Channel(name="Pricing", plugin_class="Email"),
]

router = APIRouter()


@router.get("/")
async def root():
    return channels


@router.get(
    "/{channel_id}",
    response_model=Channel_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_job(channel_id: int):
    return await Channel_Pydantic.from_queryset_single(Channels.get(id=channel_id))


@router.post("/", response_model=Channel_Pydantic)
async def create_channel(channel: ChannelIn_Pydantic):
    channel_obj = await Channels.create(**channel.dict(exclude_unset=True))
    return await Channel_Pydantic.from_tortoise_orm(channel_obj)
