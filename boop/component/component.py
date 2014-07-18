class Component(object): # ABC
    def handle_event(self, *args):
        raise NotImplemented
