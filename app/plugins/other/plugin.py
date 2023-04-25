from fastapi import BackgroundTasks


class Other:
    def other_func(self):
        print("othe stuff")

    def send_message(self, message, background_tasks: BackgroundTasks):
        print(f"Other channel: {message.description}")
