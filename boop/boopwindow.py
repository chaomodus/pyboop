import pyglet
from . import component
from . import events
from . import layereddict


class BoopWindow(component.ComponentHost, pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        self._registry = layereddict.LayeredDict()
        self._registry.push({}, 'root')

        component.ComponentHost.__init__(self)
        try:
            self.scene_manager = kwargs['scene_manager']
            del kwargs['scene_manager']
        except KeyError:
            self.scene_manager = None
        self._eventstate = events.EventStateHolder()
        self._eventstate.window = self
        self._eventstate.registry = self._registry
        # dragging objects set True and other objects may ignore
        self.dragging_veto = False
        self._exclusive_handlers = dict()
        pyglet.window.Window.__init__(self, *args, **kwargs)

    def emit_tick(self, tm):
        self.dispatch_event('on_tick', tm)

    def push_bind_exclusive(self, event_type, handler):
        self._exclusive_handlers.setdefault(event_type, [])
        self._exclusive_handlers[event_type].append(handler)

    def pop_bind_exclusive(self, event_type, handler):
        if event_type in self._exclusive_handlers:
            if handler in self._exclusive_handlers[event_type]:
                self._exclusive_handlers[event_type].remove(handler)

    def handle_pre_event(self, event_type, *args, **kwargs):
        pass

    def handle_post_event(self, event_type, result, *args, **kwargs):
        return result

    def dispatch_event(self, event_type, *args, **kwargs):
        result = None
        # let the pre event veto this event
        if self.handle_pre_event(event_type, *args, **kwargs):
            return True
        # potentially override any event handling
        if event_type in self._exclusive_handlers and self._exclusive_handlers[event_type]:
            # FIXME we need to rationalize how this propogates, because we are skipping descendent
            # handlers, so we kind of are doing the protocol that scenes implement and should
            # not do that (we should call exactly like dispatch_event, and let downstream
            # handle translating to a regular event handhler).
            #
            # Maybe we should just pass the exclusie handler in the state object?
            result = self._exclusive_handlers[event_type][-1](self._eventstate, *args, **kwargs)
        else:
            result = self.scene_manager.dispatch_event(event_type, self._eventstate, *args, **kwargs)
            # low level event handlers
            component.ComponentHost.handle_event(self, event_type, self._eventstate, *args, **kwargs)
        if not result:
            result = pyglet.window.Window.dispatch_event(self,
                                                         event_type,
                                                         *args)
        return self.handle_post_event(event_type, result, *args, **kwargs)


for event in events.boop_events:
    BoopWindow.register_event_type(event)
