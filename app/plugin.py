from typing import Protocol, List
import os
import importlib
import inspect
from fastapi import BackgroundTasks


class PluginInterface(Protocol):
    def send_message(self, message, background_tasks: BackgroundTasks):
        pass


# Create the plugin manager
class PluginManager:
    def __init__(self, plugins_path):
        self.plugins_path = plugins_path
        self.plugins: List[PluginInterface] = list()

    def load_plugin(self, plugin_class):
        # Iterate over files in the directory
        plugin_directories = [
            os.path.join(self.plugins_path, name)
            for name in os.listdir(self.plugins_path)
            if os.path.isdir(os.path.join(self.plugins_path, name))
            and name != "__pycache__"
        ]
        for plugin_directory in plugin_directories:
            for file_name in os.listdir(plugin_directory):
                # Check if the file is a Python module
                if file_name.endswith(".py") and file_name != "__init__.py":
                    # Construct the full path to the module
                    module_path = os.path.join(plugin_directory, file_name)

                    # Load the module
                    spec = importlib.util.spec_from_file_location(
                        file_name[:-3], module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    # Call a function from the module, if it exists
                    if hasattr(module, plugin_class):
                        cls = getattr(module, plugin_class)
                        plugin = cls()
                        self.plugins.append(plugin)

    def unload_plugins(self):
        pass
