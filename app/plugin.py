from typing import Protocol, List, runtime_checkable
import os
import importlib
import inspect
from fastapi import BackgroundTasks


@runtime_checkable
class PluginInterface(Protocol):
    """
    Plugin interface created with Protocol which acts as acb but in a more diynamic way.
    """

    def send_message(self, message, background_tasks: BackgroundTasks):
        pass


# Create the plugin manager
class PluginManager:
    """
    Plugin pattern implemetation
    - Search in the plugin directory for plugins implementations
    - load the plugin class in the plugin lists
    """

    def __init__(self, plugins_path):
        self.plugins_path = plugins_path
        self.plugins: List[PluginInterface] = list()

    def load_plugin(self, plugin_class):
        plugin_directories = [
            os.path.join(self.plugins_path, name)
            for name in os.listdir(self.plugins_path)
            if os.path.isdir(os.path.join(self.plugins_path, name))
            and name != "__pycache__"
        ]
        for plugin_directory in plugin_directories:
            for file_name in os.listdir(plugin_directory):
                if file_name.endswith(".py") and file_name != "__init__.py":
                    module_path = os.path.join(plugin_directory, file_name)

                    spec = importlib.util.spec_from_file_location(
                        file_name[:-3], module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, plugin_class):
                        cls = getattr(module, plugin_class)
                        plugin = cls()
                        assert isinstance(plugin, PluginInterface)
                        self.plugins.append(plugin)

    def unload_plugins(self):
        pass
