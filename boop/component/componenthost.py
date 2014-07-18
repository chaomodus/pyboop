
class ComponentHost(object):
    def __init__(self):
        self.components = list()

    def handle_event(self, *args):
        for component in self.components:
            component.handle_event(*args)
