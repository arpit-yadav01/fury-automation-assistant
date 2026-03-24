# plugins/plugin_manager.py

import os
import importlib


PLUGIN_DIR = "plugins"


class PluginManager:

    def __init__(self):

        self.plugins = {}

        self.load_plugins()

    # -----------------

    def load_plugins(self):

        if not os.path.exists(PLUGIN_DIR):
            return

        for file in os.listdir(PLUGIN_DIR):

            if not file.endswith(".py"):
                continue

            name = file[:-3]

            try:

                module = importlib.import_module(
                    f"plugins.{name}"
                )

                self.plugins[name] = module

                print("Plugin loaded:", name)

            except Exception as e:

                print("Plugin error:", name, e)

    # -----------------

    def get(self, name):

        return self.plugins.get(name)


plugin_manager = PluginManager()