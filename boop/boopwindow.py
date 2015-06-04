import pyglet
from . import component
from . import events

class BoopWindow(component.Component, pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        component.Component.__init__(self)
        try:
            self.scene_manager = kwargs['scene_manager']
            del kwargs['scene_manager']
        except KeyError:
            self.scene_manager = None

        self.eventstate = events.EventStateHolder()
        self.eventstate.window = self
        # dragging objects set True and other objects may ignore
        self.dragging_veto = False
        pyglet.window.Window.__init__(self, *args, **kwargs)

    def handle_pre_event(event_type, *args, **kwargs):
        pass

    def handle_post_event(event_type, result, *args, **kwargs):
        return result

    def dispatch_event(self, event_type, *args, **kwargs):
        result = None
        # let the pre event veto this event
        if self.handle_pre_event(event_type, *args, **kwargs):
            return True
        # potentially override any event handling
        result = self.scene_manager.dispatch_event(event_type, self.eventstate, *args)
        if not result:
            result = pyglet.window.Window.dispatch_event(self,
                                                         event_type,
                                                         *args)
        return self.handle_post_event(event_type, result, *args, **kwargs)


for event in events.boop_events:
    BoopWindow.register_event_type(event)
