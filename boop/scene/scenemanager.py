class SceneManager(object):
    def __init__(self):
        self.scenes = dict()
        self.active_scenes = list()

        self.camerax = 0
        self.cameray = 0

    def dispatch_event(self, event_type, state, *args):
        val = None
        state.scene_manger = self
        for scene in self.active_scenes:
            try:
                val = self.scenes[scene].handle_event(event_type,
                                                      state,
                                                      *args)
            except KeyError:
                pass

        return val

    def add(self, sceneobject, scene):
        self.scenes[scene] = sceneobject

    def activate(self, scene):
        try:
            self.scenes[scene].activate(self)
            self.active_scenes.append(scene)
        except KeyError:
            pass

    def deactivate(self, scene):
        try:
            self.scenes[scene].deactivate(self)
            self.active_scenes.remove(scene)
        except (ValueError, KeyError):
            pass

    def clear(self):
        for scene in self.active_scenes:
            self.scenes[scene].deactivate(self)

        self.active_scenes = list()

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
        self.move_camera(0, 0)
