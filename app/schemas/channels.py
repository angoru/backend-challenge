from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    plugin_class: str
