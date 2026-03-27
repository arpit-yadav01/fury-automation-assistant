# memory/context_engine.py

class ContextEngine:

    def __init__(self):

        self.current_goal = None
        self.current_step = None

        self.history = []
        self.task_stack = []

        self.last_result = None

    # ---------------------

    def set_goal(self, goal):

        print("Context goal:", goal)
        self.current_goal = goal

    def get_goal(self):
        return self.current_goal

    # ---------------------

    def set_step(self, step):
        self.current_step = step

    def get_step(self):
        return self.current_step

    # ---------------------

    def add_history(self, item):

        self.history.append(item)

        if len(self.history) > 50:
            self.history.pop(0)

    def get_history(self):
        return self.history

    # ---------------------

    def push_task(self, task):
        self.task_stack.append(task)

    def pop_task(self):

        if self.task_stack:
            return self.task_stack.pop()

    def get_stack(self):
        return self.task_stack

    # ---------------------

    def set_result(self, result):
        self.last_result = result

    def get_result(self):
        return self.last_result


# global
context_engine = ContextEngine()