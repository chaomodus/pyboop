from .drawable import Drawable
from pyglet.graphics import Batch


class BatchDraw(Drawable, Batch):
    """This class encapsulates both a Batch from pyglet and a Drawable from PyBoop, adapting the Batch to the Drawable
    protocol."""

    def __init__(self, window=None):
        Drawable.__init__(self, window)
        Batch.__init__(self)
        self.vx_lists = []

    def add_static(self, count, mode, group, *data):
        vx_list = Batch.add(self, count, mode, group, *data)
        self.vx_lists.append((False, vx_list))

    def add(self, count, mode, group, *data):
        vx_list = Batch.add(self, count, mode, group, *data)
        self.vx_lists.append((True, vx_list))

    def setpos(self, x, y):
        Drawable.setpos(self, x, y)

    def do_render(self, window=None):
        self.draw()
