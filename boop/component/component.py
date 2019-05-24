from .componenthost import ComponentHost

class Component(ComponentHost):
    def __init__(self):
        ComponentHost.__init__(self)
        self.state_stack = list()

    def handle_event(self, event_type, state, *args, **kwargs):
        # FIXME we should handle exceptions to an extent here
        self.state_stack.append(state)
        evthandler = None
        try:
            evthandler = self.__getattribute__('do_'+event_type)
        except AttributeError:
            try:
                evthandler = self.__getattribute__(event_type)
            except AttributeError:
                # no handler
                pass
        if evthandler:
            evthandler(state, *args, **kwargs)

        ret = ComponentHost.handle_event(self, event_type, state, *args)
        self.state_stack.pop()
        return ret
