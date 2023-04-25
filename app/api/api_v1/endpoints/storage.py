from typing import Protocol, List


class Storage(Protocol):
    def load_objects(self, return_class):
        pass


class FileStorage:
    def load_objects(self, return_class, file):
        objects = [
            return_class(name="Sales", channel="slack"),
            return_class(name="Pricing", channel="email"),
        ]
        return objects
