class SceneManager(object):
    def __init__(self):
        self.scenes = dict()
        self.active_scene = None

        self.camerax = 0
        self.cameray = 0

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

    def set_camera(self, x, y):
        self.camerax = x
        self.cameray = y
        self.dispatch_event('on_movecamera', (x, y))

    def move_camera(self, xoff, yoff):
        self.camerax += xoff
        self.cameray += yoff
        self.dispatch_event('on_movecamera', (self.camerax, self.cameray))

    def get_camera(self):
        return self.camerax, self.cameray

    def reset_camera(self):
        self.move_camera(0,0)
