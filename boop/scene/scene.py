from boop.component import Component


# note by default this acts just like a cbomponent host / component.
class Scene(Component):
    def __init__(self, window, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.window = window

    def activate(self, manager):
        pass

    def defactivate(self, manager):
        pass

    def handle_event(self, event_type, state, *args, **kwargs):
        if state:
            state.scene = self
        Component.handle_event(self,
                               event_type,
                               state,
                               *args, **kwargs)
