import os
from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse
from app.plugin import PluginManager
from dotenv import load_dotenv
from app.schemas.message import Message

router = APIRouter()


@router.post("/")
async def send_in_background(
    background_tasks: BackgroundTasks,
    message: Message,
) -> JSONResponse:
    load_dotenv()

    # TODO: get channel from message

    # TODO: get plugin class from channel

    plugin_classes = ["Email", "Slack"]

    message_plugins = PluginManager(os.getenv("PLUGIN_DIRECTORY"))
    for plugin_class in plugin_classes:
        message_plugins.load_plugin(plugin_class)

    for plugin in message_plugins.plugins:
        plugin.send_message(message, background_tasks)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
