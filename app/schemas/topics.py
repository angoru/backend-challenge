from pydantic import BaseModel


class Topic(BaseModel):
    name: str
    channel: str
