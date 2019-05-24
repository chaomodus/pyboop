import pyglet
import pyglet.font
import pyglet.text
import pyglet.graphics
import pyglet.gl as GL
from .drag import DragMixin
from . import drawtools
from .drawable import Drawable, DEBUG_DRAWABLES


# TODO automatically wrap drawtools routines (and eventually) static
# drawtools things


class DrawWrapper(Drawable):
    """Wraps a draw_* routine (or any other callable) to the Drawable
       protocol."""

    # FIXME we should provide a way to implement dimensions and other things here.

    def __init__(self, display, drawtool, *args, **kwargs):
        Drawable.__init__(self, display)
        self.drawtool = drawtool
        self.dt_args = args
        self.dt_kwargs = kwargs
        self.display = display

    def do_render(self, display):
        self.drawtool(*self.dt_args, **self.dt_kwargs)


class DraggableDrawableMixin(DragMixin):
    """Mix this with a Drawable to allow the drawable to be dragged and dropped."""

    _ddm_offset = (0, 0)

    def can_drag(self, state, x, y):
        return self.point_hit_test(x, y)

    def start_drag(self, state, x, y):
        px, py = self.getpos()
        self._ddm_offset = (px - x, py - y)
        return True

    def end_drag(self, state, x, y):
        self.setpos(x + self._ddm_offset[0], y + self._ddm_offset[1])
        self._ddm_offset = (0, 0)

    def dragging(self, state, x, y):
        self.setpos(x + self._ddm_offset[0], y + self._ddm_offset[1])


# Proof of concept, probably not a good thing to actually use.
class Clear(Drawable):
    """This is a proof of concept, and should probably not be used (put a window.clear in the render_* for the Scene or
    decorative Drawable)."""

    def do_render(self, window):
        window.clear()


class Image(Drawable):
    """Wraps pyglet's Sprite in Drawable protocol. Not effecient if there are many sprites."""

    # FIXME implement BAG OF IMAGE type which has dirtyness setting and only reloads sprites into a
    # batch if they are dirty.
    def __init__(self, display, imgobj, position=(0, 0), z=0.0):
        Drawable.__init__(self, display)
        self.spr = pyglet.sprite.Sprite(imgobj)
        self.spr.z = float(z)
        self.setpos(*position)

    def rotate(self, rotation):
        self.spr.rotation = float(rotation)
        self.setpos(*self.spr.position)

    def setscale(self, scale):
        self.spr.scale = scale

    def getsize(self):
        return self.spr.width, self.spr.height

    def do_render(self, display):
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        self.spr.draw()

        if DEBUG_DRAWABLES:
            # debug crosshair
            pos = self.spr.position
            # red crosshair indicates anchor position
            drawtools.draw_crosshair(pos[0], pos[1], color=(1.0, 0.0, 0.0))
            # cyan crosshair indicates sprite position (should be the same
            # as drawable position)
            drawtools.draw_crosshair(pos[0], pos[1], color=(0.0, 1.0, 1.0))


class Backdrop(Image):
    """A deprecated proof of concept that draws a large image the size of the window it's placed in."""

    def __init__(self, display, imgobj):
        Image.__init__(self, display, imgobj, position=(0, 0))
        scale = 0
        if self.spr.width > self.spr.height:
            scale = display.width / float(self.spr.width)
        else:
            scale = display.height / float(self.spr.height)
        self.spr.scale = scale

    def do_render(self, display):
        # if self.spr.width > self.spr.height:
        #     scale = display.width / float(self.spr.width)
        # else:
        #     scale = display.height / float(self.spr.height)
        # self.spr.scale = scale
        self.spr.draw()
        # Image.render(self,display)


class Label(Drawable):
    """Wraps Pyglet's Label in the Drawable protocol."""

    def __init__(
        self,
        display,
        text,
        font_name="Helvetica",
        font_size=12,
        position=(0, 0),
        color=(1.0, 1.0, 1.0, 1.0),
        anchor_x="left",
        anchor_y="bottom",
        align="left",
        bold=False,
        width=None,
        multiline=False,
    ):

        Drawable.__init__(self, display)
        self.text = text
        self.position = position
        if len(color) != 4:
            pygcolor = list(map(lambda x: int(round(x * 255)), (color[0], color[1], color[2], 1.0)))
        else:
            pygcolor = list(map(lambda x: int(round(x * 255)), color))

        self.label = pyglet.text.Label(
            text=text,
            font_name=font_name,
            font_size=font_size,
            x=0.0,
            y=0.0,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            align=align,
            bold=bold,
            multiline=multiline,
            color=pygcolor,
            width=width,
        )

    def setalpha(self, alpha):
        c = list(self.label.color)
        c[3] = int(round(alpha * 255))
        self.label.color = c

    def getalpha(self):
        return self.label.color[3] / 255.0

    def do_render(self, display):
        if self.getalpha() != 0:
            self.label.draw()


class LabelOld(Drawable):
    """Wraps pyglet's text object class in Drawable protocol."""

    def __init__(self, display, font, text="", position=(0, 0), color=(1.0, 1.0, 1.0, 1.0), width=None):
        Drawable.__init__(self, display)
        self.text = text
        self.position = position
        self.txtobj = pyglet.font.Text(font, text, 0.0, 0.0, color, width=width)
        if len(color) != 4:
            color = (color[0], color[1], color[2], 1.0)
        self.txtobj.color = color
        self.txtobj.z = 0.0

    def setalpha(self, alpha):
        c = list(self.txtobj.color)
        c[3] = alpha
        self.txtobj.color = c

    def getalpha(self):
        return self.txtobj.color[3]

    def do_render(self, display):
        # self.txtobj.x = float(self.position[0])
        # self.txtobj.y = float(self.position[1])
        # self.txtobj.z = 0.0
        self.txtobj.draw()


class FadeMixin(object):
    """Mix this with your Drawable which supports alpha in order to fade it in and out using tick events."""

    FADE_ST_ON, FADE_ST_OFF, FADE_ST_FO, FADE_ST_FI = range(4)

    def __init__(self, *args, **kwargs):
        self.fade_state = self.FADE_ST_ON
        self.fade_rate = 0.05

    def fade_toggle(self):
        if self.fade_state in (self.FADE_ST_ON, self.FADE_ST_FI):
            self.fade_state = self.FADE_ST_FO
        else:
            self.fade_state = self.FADE_ST_FI

    def fade_in(self):
        self.fade_state = self.FADE_ST_FI

    def fade_out(self):
        self.fade_state = self.FADE_ST_FO

    def fade_update(self):
        if self.fade_state != self.FADE_ST_OFF:
            if self.fade_state in (self.FADE_ST_FO, self.FADE_ST_FI):
                alpha = self.getalpha()
                if self.fade_state == self.FADE_ST_FO:
                    alpha -= self.fade_rate
                    if alpha <= 0.0:
                        alpha = 0.0
                        self.fade_state = self.FADE_ST_OFF
                else:
                    alpha += self.fade_rate
                    if alpha >= 1.0:
                        alpha = 1.0
                        self.fade_state = self.FADE_ST_ON
                self.setalpha(alpha)


class DraggableImage(Image, DraggableDrawableMixin):
    """An Image that's also Draggable. Deprecated proof of concept that may not be useful in practice."""

    def __init__(self, window, image):
        DraggableDrawableMixin.__init__(self)
        Image.__init__(self, window, image)


class ClockDisplay(Drawable):
    """Simple display for FPS counter."""

    # fixme apparently this is inaccurate according to docs. newer pyglet has fix.
    # fixme map normal drawable parms to this (fps.label is a regular label object).
    def __init__(self, window, *args, **kwargs):
        Drawable.__init__(self, window)
        self.fps = pyglet.clock.ClockDisplay(*args, **kwargs)

    def do_render(self, *args, **kwargs):
        self.fps.draw()
