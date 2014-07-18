import pyglet

class BoopWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        try:
            self.scene_manager = kwargs['scene_manager']
            del kwargs['scene_manager']
        except KeyError:
            self.scene_manager = None

        pyglet.window.Window.__init__(self, *args, **kwargs)

    def dispatch_event(self, event_type, *args):
        result = None
        try:
            result = self.scene_manager.dispatch_event(self, event_type, *args)
        except:
            pass
        if not result:
            pyglet.window.Window.dispatch_event(self, event_type, *args)
