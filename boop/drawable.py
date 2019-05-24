import pyglet.gl as GL

from .component import Component

DEBUG_DRAWABLES = False


class Drawable(Component):
    """This is the base class for drawable things within PyBoop. It provides most of the background machinery and a
    basic protocol for drawable things."""

    def __init__(self, window):
        Component.__init__(self)
        self.position = (0, 0)
        self.size = (0, 0)
        self.window = window

    def getsize(self):
        """Returns the rectangle size."""
        return self.size

    def getpos(self):
        """Returns the position of the lower left corner."""
        return self.position

    @property
    def x(self):
        return self.getpos()[0]

    @property
    def y(self):
        return self.getpos()[1]

    def setpos(self, x, y):
        """Sets the position of the lowel left corner."""
        self.position = (x, y)

    def setsize(self, x, y):
        """Sets the rectangle size."""
        self.size = (x, y)

    def getrect(self):
        """Returns the rectangle coordinates."""
        sz = self.getsize()
        pos = self.getpos()
        return (pos[0], pos[1], pos[0] + sz[0], pos[1] + sz[1])

    def setalpha(self, alpha):
        """Sets the draw alpha of this object if applicable."""
        pass

    def getalpha(self):
        """Returns the set draw alpha."""
        return 1.0

    def point_hit_test(self, px, py):
        """Returns True if a point is within (logically) part of this object."""
        r = self.getrect()
        return px > r[0] and px < r[2] and py > r[1] and py < r[3]

    def on_draw(self, state):
        """This is called each frame if this object is in the drawing context (within a Scene or other drawable
        component)"""
        self.render(state.window)

    def render(self, window):
        """Overriding this is deprecated. Override render_at or do_render instead."""
        pos = self.getpos()
        self.render_at(window, pos[0], pos[1], 0.0)

    def render_at(self, window, x, y, z=0.0):
        """Performs the repositioning so that drawing happens at 0,0 and then calls do_render."""
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix()
        GL.glLoadIdentity()
        GL.glTranslatef(float(x), float(y), float(z))
        self.do_render(window)
        GL.glPopMatrix()

    def do_render(self, window):
        """Override this. Draw the thing around 0,0"""
        pass
