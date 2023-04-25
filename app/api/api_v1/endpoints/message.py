import os
from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse
from app.plugin import PluginManager
from dotenv import load_dotenv
from app.schemas.message import Message
from app.models import Topics, Topic_Pydantic, Channels, Channel_Pydantic

router = APIRouter()


@router.post("/")
async def send_in_background(
    background_tasks: BackgroundTasks,
    message: Message,
) -> JSONResponse:
    load_dotenv()

    topic = await Topics.get(name=message.topic).prefetch_related("channel")

    plugin_classes = []
    plugin_classes.append(topic.channel.plugin_class)

    message_plugins = PluginManager(os.getenv("PLUGIN_DIRECTORY"))
    for plugin_class in plugin_classes:
        message_plugins.load_plugin(plugin_class)

    for plugin in message_plugins.plugins:
        plugin.send_message(message, background_tasks)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
