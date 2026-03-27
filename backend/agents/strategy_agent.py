from agents.base_agent import BaseAgent
from brain.strategy_engine import build_strategy


class StrategyAgent(BaseAgent):

    def __init__(self):
        super().__init__("StrategyAgent")

    def can_handle(self, task):

        if not isinstance(task, dict):
            return False

        return task.get("intent") == "goal_task"

    def handle(self, task):

        data = task.get("data")

        strategy = build_strategy(data)

        if not strategy:
            return task

        print("Strategy built:", len(strategy), "steps")

        return {
            "intent": "workflow",
            "workflow": strategy,
            "source": "strategy_engine"
        }