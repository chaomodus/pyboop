from .componenthost import ComponentHost


class Component(ComponentHost):
    def __init__(self):
        ComponentHost.__init__(self)

    def handle_event(self, event_type, *args, **kwargs):
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
            evthandler(self, *args, **kwargs)

        return ComponentHost.handle_event(self, event_type, *args)
