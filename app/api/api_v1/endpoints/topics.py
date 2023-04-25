from fastapi import APIRouter
from app.schemas.topics import Topic
from app.models import Topics, Topic_Pydantic, TopicIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

topics = [
    Topic(name="Sales", channel="slack"),
    Topic(name="Pricing", channel="email"),
]


router = APIRouter()


@router.get("/")
async def root():
    return topics


@router.get(
    "/{topic_id}",
    response_model=Topic_Pydantic,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_job(topic_id: int):
    return await Topic_Pydantic.from_queryset_single(Topics.get(id=topic_id))


@router.post("/", response_model=Topic_Pydantic)
async def create_topic(topic: TopicIn_Pydantic):
    topic_obj = await Topics.create(**topic.dict(exclude_unset=True))
    return await Topic_Pydantic.from_tortoise_orm(topic_obj)
