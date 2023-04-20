import os
from typing import List

from fastapi import APIRouter, BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

import app.plugins


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Message(BaseModel):
    topic: str
    description: str


router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="username",
    MAIL_PASSWORD="**********",
    MAIL_FROM="test@email.com",
    MAIL_PORT=os.getenv("EMAIL_PORT"),
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)


@router.post("/")
async def send_in_background(
    background_tasks: BackgroundTasks,
    message: Message,
) -> JSONResponse:
    # create message object

    # get channel from message

    # get plugin class from channel

    plugin_class = "Email"

    # implement plugin
    import os
    import importlib.util

    # Directory containing plugins
    plugins_dir = "/code/app/plugins"

    # Iterate over files in the directory
    for file_name in os.listdir(plugins_dir):
        # Check if the file is a Python module
        if file_name.endswith(".py") and file_name != "__init__.py":
            # Construct the full path to the module
            module_path = os.path.join(plugins_dir, file_name)

            # Load the module
            spec = importlib.util.spec_from_file_location(file_name[:-3], module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Call a function from the module, if it exists
            if hasattr(module, plugin_class):
                cls = getattr(module, plugin_class)
                plugin = cls()

    plugin.send()

    # execute plugin send message
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=["wadus@example.com"],
        body="Simple background task",
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
