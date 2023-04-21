from pydantic import BaseModel


class Message(BaseModel):
    topic: str
    description: str
