from .componenthost import ComponentHost
import sys
DEBUG=False

class Component(ComponentHost):
    def __init__(self):
        ComponentHost.__init__(self)

    def handle_event(self, event_type, *args, **kwargs):
        if DEBUG:
            if len(args):
                sys.stdout.write('handle_event: '+str(self)+' event_type='+str(event_type)+' '+str(args)+'\n')
            else:
                sys.stdout.write('handle_event: '+str(self)+' called with no args\n')
        evthandler = None
        try:
            evthandler = self.__getattribute__('do_'+event_type)
        except AttributeError:
            try:
                evthandler = self.__getattribute__(event_type)
            except AttributeError:
                DEBUG and sys.stdout.write('handle_event: '+str(self)+' event_type='+str(event_type)+' '+str(args)+'NO HANDLER\n')

        if evthandler:
            evthandler(self, *args, **kwargs)

        return ComponentHost.handle_event(self, event_type, *args)
