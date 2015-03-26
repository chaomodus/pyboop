import sys
DEBUG=False

class SceneManager(object):
    def __init__(self):
        self.scenes = dict()
        self.active_scenes = set()

        self.camerax = 0
        self.cameray = 0

    def dispatch_event(self, event_type, window, *args):
        ret = None
        val = None
        DEBUG and sys.stdout.write('dispatch_event: '+str(self)+' '+str(window)+' '+str(event_type)+' '+str(args)+'\n')
        for scene in self.active_scenes:
            try:
                val = self.scenes[scene].handle_event(event_type, window, self, *args)
                if val is not None:
                    ret = val
            except KeyError:
                pass

        return val

    def add(self, sceneobject, scene):
        self.scenes[scene] = sceneobject

    def activate(self, scene):
        try:
            self.scenes[scene].activate(self)
            self.active_scenes.add(scene)
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
        self.move_camera(0,0)
