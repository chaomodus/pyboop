
class ComponentHost(object):
    def __init__(self):
        self.components = list()

    def handle_event(self, event_type, state, *args, **kwargs):
        state.container = self
        for component in self.components:
            component.handle_event(event_type, state, *args, **kwargs)

    def add(self, component):
        self.components.append(component)

    def remove(self, component):
        try:
            self.components.remove(component)
        except ValueError:
            return None
        return component
