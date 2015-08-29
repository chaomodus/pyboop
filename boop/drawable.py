DEBUG_DRAWABLES = False

from .component import Component

# abc
class Drawable(Component):
    def __init__(self, window):
        Component.__init__(self)
        self.position = (0, 0)
        self.window = window

    def getsize(self):
        return (0, 0)

    def getpos(self):
        return self.position

    @property
    def x(self):
        return self.getpos()[0]

    @property
    def y(self):
        return self.getpos()[1]

    def setpos(self, x, y):
        self.position = (x, y)

    def getrect(self):
        sz = self.getsize()
        pos = self.getpos()
        return (pos[0],
                pos[1],
                pos[0] + sz[0],
                pos[1] + sz[1])

    def setalpha(self, alpha):
        pass

    def getalpha(self):
        return 1.0

    def render(self, window):
        pass

    def point_hit_test(self, px, py):
        r = self.getrect()
        return px > r[0] and px < r[2] and py > r[1] and py < r[3]

    def on_draw(self, state):
        self.render(state.window)
