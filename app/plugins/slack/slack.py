from fastapi import BackgroundTasks
from typing import Protocol


class Slack:
    def other_func(self):
        print("othe stuff")

    def send_message(self, message, background_tasks: BackgroundTasks):
        print("slack email")
