class BasePlatform:
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def turn_display_on(self):
        pass

    def turn_display_off(self):
        pass
