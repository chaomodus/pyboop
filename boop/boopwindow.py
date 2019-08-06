from pyglet.window import Window
from .componenthost import ComponentHost
from .events import EventStateHolder, boop_events
from .layereddict import LayeredDict


class BoopWindow(ComponentHost, Window):
    """This in a subclass of pyglet's Window class that provides some convience for the fan-out event handling, and also
    makes it follow the Component protocol."""

    def __init__(self, *args, **kwargs):
        self._registry = LayeredDict()
        self._registry.push({}, "root")

        ComponentHost.__init__(self)
        try:
            self.scene_manager = kwargs["scene_manager"]
            del kwargs["scene_manager"]
        except KeyError:
            self.scene_manager = None
        self._eventstate = EventStateHolder()
        self._eventstate.window = self
        self._eventstate.registry = self._registry
        # dragging objects set True and other objects may ignore
        self.dragging_veto = False
        self._exclusive_handlers = dict()
        Window.__init__(self, *args, **kwargs)

    def emit_tick(self, tm):
        """Tick is a periodic time event."""
        self.dispatch_event("on_tick", tm)

    def push_bind_exclusive(self, event_type, handler):
        """Take over exclusive handling of a specific event_type (pushes event handler to top of stack)."""
        self._exclusive_handlers.setdefault(event_type, [])
        self._exclusive_handlers[event_type].append(handler)

    def pop_bind_exclusive(self, event_type, handler):
        "Pops the top of the exclusive event handler stack and restores normal handling if the stack is empty." ""
        if event_type in self._exclusive_handlers:
            if handler in self._exclusive_handlers[event_type]:
                self._exclusive_handlers[event_type].remove(handler)

    def handle_pre_event(self, event_type, *args, **kwargs):
        """This is called immediately before the Window handles an event. It may veto the event from calling any
        handlers."""
        pass

    def handle_post_event(self, event_type, result, *args, **kwargs):
        """This is called immeditaley after the Window handles an event."""
        return result

    def dispatch_event(self, event_type, *args, **kwargs):
        """Override all of pyglet's event handling for our span out model."""
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
            ComponentHost.handle_event(self, event_type, self._eventstate, *args, **kwargs)
        if not result:
            result = Window.dispatch_event(self, event_type, *args)
        return self.handle_post_event(event_type, result, *args, **kwargs)


for event in boop_events:
    BoopWindow.register_event_type(event)
