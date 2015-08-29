from .drawable import Drawable
from pyglet.graphics import Batch
from .utils import chunker

class BatchDraw(Drawable, Batch):
    def __init__(self, window=None):
        Drawable.__init__(self, window)
        Batch.__init__(self)
        self.vx_lists = []

    def add_static(self, count, mode, group, *data):
        vx_list = Batch.add(self, count, mode, group, *data)
        self.vx_lists.append((False, vx_list))

    def add(self, count, mode, group, *data):
        vx_list = Batch.add(self, count, mode, group, *data)
        pos = self.getpos()
        if not pos == (0, 0):
            self._update_vx_list_pos(vx_list, pos)
        self.vx_lists.append((True, vx_list))

    def setpos(self, x, y):
        for vx_list in self.vx_lists:
            if vx_list[0]:
                self._update_vx_list_pos(vx_list[1], (x, y))
        Drawable.setpos(self, x, y)

    def _update_vx_list_pos(self, vx_list, pos):
        # tihs seems dreadfully inefficient but i guess we could trade memory for
        # efficiency (remove the extra card fetch by saving the original vertices
        # before positioning).
        comps = len(vx_list.vertices) // vx_list.count
        oldpos = self.getpos()
        for vert in chunker(range(0, len(vx_list.vertices)), comps):
            nvx = vx_list.vertices[vert[0]] - oldpos[0]
            nvy = vx_list.vertices[vert[1]] - oldpos[1]
            vx_list.vertices[vert[0]] = (nvx + pos[0])
            vx_list.vertices[vert[1]] = (nvy + pos[1])

    def render(self):
        self.draw()
