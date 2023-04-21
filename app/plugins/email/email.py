from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
import os
from dotenv import load_dotenv


class Email:
    def send_message(self, message, background_tasks: BackgroundTasks):
        load_dotenv()
        conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=os.getenv("MAIL_PORT"),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
            MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
            MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),
            USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"),
            VALIDATE_CERTS=os.getenv("VALIDATE_CERTS"),
        )

        mail_message = MessageSchema(
            subject="A mail from the bot",
            recipients=[os.getenv("MAIL_TO")],
            body=message.description,
            subtype=MessageType.plain,
        )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, mail_message)
