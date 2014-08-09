from .componenthost import ComponentHost
class Component(ComponentHost):
    def __init__(self):
        ComponentHost.__init__(self)

    def handle_event(self, *args):
        if len(args):
            evt = args[0]
            try:
                evthandler = self.__getattribute__('do_'+evt)
                evthandler(self, *args)
            except AttributeError:
                pass

        return ComponentHost.handle_event(self, *args)
