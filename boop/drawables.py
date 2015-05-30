import pyglet
import pyglet.font
import pyglet.graphics
import pyglet.gl as GL
from .component import Component
from . import drawtools

# FIXME all of this crap should use static vertex lists. We should also
# consider wrapping the other drawables in drawtools.

# TODO automatically wrap drawtools routines (and eventually) static
# drawtools things

DEBUG_DRAWABLES = False


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
        if DEBUG_DRAWABLES:
            # debug rectangle
            pos = self.getpos()
            sz = self.getsize()
            drawtools.draw_gradbox((1.0, 0.0, 0.0, 0.25), (1.0, 0.0, 0.0, 0.125), position=pos, size=sz)
            drawtools.draw_crosshair(pos[0], pos[1], color=(1.0, 1.0, 0.0))


class DrawWrapper(Drawable):
    """Wraps a draw_* routine (or any other callable) to the Drawable
       protocol."""

    def __init__(self, display, drawtool, *args, **kwargs):
        Drawable.__init__(self, display)
        self.drawtool = drawtool
        self.dt_args = args
        self.dt_kwargs = kwargs
        self.display = display

    def render(self, display):
        self.drawtool(*self.dt_args, **self.dt_kwargs)


class DragMixin(object):
    _dragging = False
    _dragoffset = (0, 0)

    def on_mouse_drag(self, state, x, y, dx, dy, buttons, modifiers):
        if (buttons & pyglet.window.mouse.LEFT) and not self._dragging and self.point_hit_test(x, y) and not state.window.dragging_veto:
            self._dragging = True
            state.window.dragging_veto = self
            px, py = self.getpos()
            self._dragoffset = (px - x, py - y)
        elif self._dragging:
            if not (buttons & pyglet.window.mouse.LEFT):
                self._dragging = False
            else:
                self.setpos(x+self._dragoffset[0], y+self._dragoffset[1])

    def on_mouse_release(self, state, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT:
            self._dragging = False
            if state.window.dragging_veto is self:
                state.window.dragging_veto = False
            state.handled = True


class Clear(Drawable):
    def render(self, window):
        window.clear()


class Image(Drawable):
    def __init__(self, display, imgobj, position=(0, 0)):
        Drawable.__init__(self, display)
        self.spr = pyglet.sprite.Sprite(imgobj)
        self.spr.z = 0.0
        self.setpos(*position)

    def getpos(self):
        pos = Drawable.getpos(self)
        return pos

    def setpos(self, x, y):
        Drawable.setpos(self, x, y)
        self.spr.position = (x, y)

    def rotate(self, rotation):
        self.spr.rotation = float(rotation)
        self.setpos(*self.spr.position)
        # fixme calculate new rectangle based on rotated points (width and
        # height aren't fixed by pyglet) note that it rotates around 0,0
        # regardless of anchor, which may make the transformation
        # much easier to deal with.

        # self.width = self.spr.width
        # self.height = self.spr.height

    def getsize(self):
        return self.spr.width, self.spr.height

    def render(self, display):
        # self.spr.x = float(self.position[0])
        # self.spr.y = float(self.position[1])
        # self.spr.z = 0.0
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        self.spr.draw()

        if DEBUG_DRAWABLES:
            # debug crosshair
            pos = self.spr.position
            # red crosshair indicates anchor position
            drawtools.draw_crosshair(pos[0],
                                     pos[1],
                                     color=(1.0, 0.0, 0.0))
            # cyan crosshair indicates sprite position (should be the same
            # as drawable position)
            drawtools.draw_crosshair(pos[0], pos[1], color=(0.0, 1.0, 1.0))



class Backdrop(Image):
    def __init__(self, display, imgobj):
        Image.__init__(self, display, imgobj, position=(0, 0))
        scale = 0
        if self.spr.width > self.spr.height:
            scale = display.width / float(self.spr.width)
        else:
            scale = display.height / float(self.spr.height)
        self.spr.scale = scale

    def render(self, display):
        # if self.spr.width > self.spr.height:
        #     scale = display.width / float(self.spr.width)
        # else:
        #     scale = display.height / float(self.spr.height)
        # self.spr.scale = scale
        self.spr.draw()
        # Image.render(self,display)


class Label(Drawable):
    def __init__(self,
                 display,
                 font,
                 text='',
                 position=(0, 0),
                 color=(1, 1, 1, 1),
                 width=None):
        Drawable.__init__(self, display)
        self.text = text
        self.position = position
        self.txtobj = pyglet.font.Text(font,
                                       text,
                                       float(position[0]),
                                       float(position[1]),
                                       color,
                                       width=width)
        self.txtobj.z = 0.0

    def setalpha(self, alpha):
        c = list(self.txtobj.color)
        c[3] = alpha
        self.txtobj.color = c

    def getalpha(self):
        return self.txtobj.color[3]

    def render(self, display):
        # self.txtobj.x = float(self.position[0])
        # self.txtobj.y = float(self.position[1])
        # self.txtobj.z = 0.0
        self.txtobj.draw()


class FadeMixin(object):
    FADE_ST_ON, FADE_ST_OFF, FADE_ST_FO, FADE_ST_FI = range(4)

    def __init__(self, *args, **kwargs):
        self.fade_state = self.FADE_ST_ON

    def fade_toggle(self):
        if self.fade_state in (self.FADE_ST_ON, self.FADE_ST_FI):
            self.fade_state = self.FADE_ST_FO
        else:
            self.fade_state = self.FADE_ST_FI

    def fade_update(self):
        if self.fade_state != self.FADE_ST_OFF:
            if self.fade_state in (self.FADE_ST_FO, self.FADE_ST_FI):
                alpha = self.getalpha()
                if self.fade_state == self.FADE_ST_FO:
                    alpha -= 0.05
                    if alpha <= 0.0:
                        alpha = 0.0
                        self.fade_state = self.FADE_ST_OFF
                else:
                    alpha += 0.05
                    if alpha >= 1.0:
                        alpha = 1.0
                        self.fade_state = self.FADE_ST_ON
                self.setalpha(alpha)


class DraggableImage(Image, DragMixin):
    def __init__(self, window, image):
        Image.__init__(self, window, image)
        DragMixin.__init__(self)
