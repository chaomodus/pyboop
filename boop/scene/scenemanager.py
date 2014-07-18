class SceneManager(object):
    def __init__(self):
        self.scenes = dict()
        self.active_scene = None

    def dispatch_event(self, window, event_type, *args):
        try:
            return self.scenes[self.active_scene].handle_event(window, self, event_type, *args)
        except KeyError:
            return None

    def activate_scene(self, scene):
        try:
            self.scenes[scene].activate(self)
            self.active_scene = scene
        except KeyError:
            pass

    # fixme I think the api could be a bit more useful here
