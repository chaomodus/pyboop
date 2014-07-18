from boop.component import ComponentHost

class Scene(ComponentHost): # ABC
    def __init__(self, *args, **kwargs):
        ComponentHost.__init__(self, *args, **kwargs)

    def activate(self, manager):
        pass

    # note by default this acts just like a component host.
