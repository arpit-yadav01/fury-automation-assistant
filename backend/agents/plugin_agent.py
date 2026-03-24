# agents/plugin_agent.py

from agents.base_agent import BaseAgent

from plugins.plugin_manager import plugin_manager


class PluginAgent(BaseAgent):

    def __init__(self):
        super().__init__("PluginAgent")

    # -----------------

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        if task.get("plugin"):
            return True

        return False

    # -----------------

    def handle(self, task):

        name = task.get("plugin")

        data = task.get("data", {})

        mod = plugin_manager.get(name)

        if not mod:
            print("Plugin not found:", name)
            return

        if hasattr(mod, "run"):

            return mod.run(data)

        print("Plugin has no run()")