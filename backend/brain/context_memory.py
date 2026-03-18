# brain/context_memory.py


class ContextMemory:

    def __init__(self):

        self.current_app = None
        self.current_window = None
        self.last_site = None
        self.last_file = None
        self.last_action = None

    # ---------------------

    def set_app(self, app):

        print("Memory app:", app)

        self.current_app = app

    # ---------------------

    def set_window(self, window):

        print("Memory window:", window)

        self.current_window = window

    # ---------------------

    def set_site(self, site):

        print("Memory site:", site)

        self.last_site = site

    # ---------------------

    def set_file(self, file):

        print("Memory file:", file)

        self.last_file = file

    # ---------------------

    def set_action(self, action):

        self.last_action = action

    # ---------------------

    def get_app(self):
        return self.current_app

    def get_window(self):
        return self.current_window

    def get_site(self):
        return self.last_site

    def get_file(self):
        return self.last_file

    def get_action(self):
        return self.last_action


# global memory

memory = ContextMemory()