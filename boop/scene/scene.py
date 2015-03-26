from boop.component import ComponentHost

class Scene(ComponentHost): # ABC
    def __init__(self, window, *args, **kwargs):
        ComponentHost.__init__(self, *args, **kwargs)
        self.window = window

    def activate(self, manager):
        pass

    def defactivate(self, manager):
        pass

    def handle_event(self, event_type, window, scene_manager, *args):
        ComponentHost.handle_event(self, event_type, window, scene_manager, *args)

    # note by default this acts just like a cbomponent host.
