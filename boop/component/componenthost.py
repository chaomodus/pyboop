
class ComponentHost(object):
    def __init__(self):
        self.components = list()

    def handle_event(self, event_type, *args, **kwargs):
        for component in self.components:
            component.handle_event(event_type, *args, **kwargs)

    def add(self, component):
        self.components.append(component)
