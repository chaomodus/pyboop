import pyglet
import pyglet.font
import pyglet.gl as GL
import pyglet.graphics
import itertools
from .component import Component

#abc
class Drawable(Component):
    def __init__(self, window):
        Component.__init__(self)
        self.position = (0,0)
        self.window = window
        pass

    def getsize(self):
        return (0,0)

    def getpos(self):
        return self.position

    def setpos(self, x, y):
        self.position = (x,y)

    def setalpha(self, alpha):
        pass

    def getalpha(self):
        return 1.0

    def render(self, window):
        pass

    def on_draw(self, *args, **kwargs):
        self.render(self.window)

class Clear(Drawable):
    def render(self, window):
        window.clear()

class Image(Drawable):
    def __init__(self, display, imgobj, position=(0,0)):
        Drawable.__init__(self, display)
        self.spr  = pyglet.sprite.Sprite(imgobj, float(position[0]), float(position[1]))
        self.spr.z = 0.0

    def render(self, display):
        # self.spr.x = float(self.position[0])
        # self.spr.y = float(self.position[1])
        # self.spr.z = 0.0
        self.spr.draw()

class Backdrop(Image):
    def __init__(self, display, imgobj):
        Image.__init__(self, display, imgobj, position=(0,0))
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
    def __init__(self, display, font,  text='',  position=(0,0), color=(1,1,1,1)):
        Drawable.__init__(self, display)
        self.text = text
        self.position = position
        self.txtobj = pyglet.font.Text(font, text, float(position[0]), float(position[1]), color)
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

class LineBox(Drawable):
    def __init__(self, display, color=(1.0,1.0,1.0), position=(0,0), size=(0,0)):
        Drawable.__init__(self, display)

class GradBox(Drawable):
    def __init__(self, display, startcolor=(0.0,0.0,0.0), endcolor=(0.0,0.0,0.0), vertical=True ,position=(0,0), size=(0,0)):
        Drawable.__init__(self, display)

        self.startcolor = startcolor
        self.endcolor = endcolor

        self.vertical = vertical

        self.position = position
        self.size = size

        self.z = 0.0

    def render(self, display):
        self.z = float(self.z)
        startcoords = [float(x) for x in self.position]
        endcoords = [float(x + y) for x, y in zip(self.position, self.size)]

        # GL.glBegin(GL.GL_QUADS)
        # if self.vertical:
        #     GL.glColor3f(*self.startcolor)
        #     GL.glVertex3f(startcoords[0], startcoords[1], self.z)
        #     GL.glVertex3f(startcoords[0], endcoords[1], self.z)
        #     GL.glColor3f(*self.endcolor)
        #     GL.glVertex3f(endcoords[0], endcoords[1], self.z)
        #     GL.glVertex3f(endcoords[0], startcoords[1], self.z)
        # else:
        #     GL.glColor3f(*self.startcolor)
        #     GL.glVertex3f(endcoords[0], startcoords[1], self.z)
        #     GL.glVertex3f(startcoords[0], startcoords[1], self.z)
        #     GL.glColor3f(*self.endcolor)
        #     GL.glVertex3f(startcoords[0], endcoords[1], self.z)
        #     GL.glVertex3f(endcoords[0], endcoords[1], self.z)
        # GL.glEnd()

        if self.vertical:
            pyglet.graphics.draw(4, GL.GL_QUADS,
                                 ('v3f', (startcoords[0], startcoords[1], self.z,
                                          startcoords[0], endcoords[1], self.z,
                                          endcoords[0], endcoords[1], self.z,
                                          endcoords[0], startcoords[1], self.z)),
                                 ('c3f', list(itertools.chain(self.startcolor,
                                                              self.startcolor,
                                                              self.endcolor,
                                                              self.endcolor))))
        else:
            pyglet.graphics.draw(4, GL.GL_QUADS,
                                 ('v3f',(startcoords[0], startcoords[1], self.z,
                                         startcoords[0], endcoords[1], self.z,
                                         endcoords[0], endcoords[1], self.z,
                                         endcoords[0], startcoords[1], self.z)),
                                 ('c3f', list(itertools.chain(self.startcolor,
                                                              self.endcolor,
                                                              self.endcolor,
                                                              self.startcolor))))
