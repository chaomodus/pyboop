# -*- coding: utf-8 -*-
# NOTE! THis file will change frequently as features are developed and used.
# Examples of developed frameworks and uses will be spun off into separate files as needed.
# Current use: developing menus for menu-based games (dating games etc.)
#
import sys
sys.path.append('../')
import pyglet
import pyglet.font
import pyglet.gl as GL
import pyglet.graphics
import boop
import boop.component
import boop.scene
from boop.drawables import Drawable
import boop.drawtools
import math
import random

class MyScene(boop.scene.Scene):
    def __init__(self, window):
        boop.scene.Scene.__init__(self, window)
        self.components.append(boop.drawables.Clear(window))


class MouseXhair(Drawable):
    def __init__(self, window):
        Drawable.__init__(self, window)
        window.set_mouse_visible(False)
        self.mousex = 0
        self.mousey = 0

    def render(self, window):
        # mouse is more responsive if we aren't event driven?? We don't have to wait for the events to by dispatched etc.
        # this points to a flaw in the way we propogate events, we should probably optimize at runtime by scanning the object tree
        # and only subscribing active end points to the event handhler
        boop.drawtools.draw_crosshair(window._mouse_x, window._mouse_y)

class TestLine(Drawable):
    def __init__(self, window):
        Drawable.__init__(self, window)
        self.lines = pyglet.graphics.Batch()
        self.arrows = pyglet.graphics.Batch()
        x = 100
        y = 500
        for i in range(0, 100, 10):
            boop.drawtools.make_thickline((x, y), (x + (100 * math.cos(math.pi * 2 * (i / 100.0))), y + (100 * math.sin(math.pi * 2 * (i / 100.0)))), i / 10, color=(1.0 - i / 100.0, i / 100.0, i / 100.0, 1.0), batch=self.lines)
        x = (window.width / 2) + 200
        y = (window.height / 2) + 200
        for i in range(0, 100, 10):
            boop.drawtools.make_arrow((x, y), (x + (100 * math.cos(math.pi * 2 * (i / 100.0))), y + (100 * math.sin(math.pi * 2 * (i / 100.0)))), color=(i / 100.0, i / 100.0, 1.0 - i / 100.0, 1.0), batch=self.arrows)


    def render(self, window):
        self.lines.draw()
        self.arrows.draw()

config = pyglet.gl.Config(sample_buffers=1,
                          samples=4,
                          double_buffer=1,
                          depth_size=8)

fnt = pyglet.font.load('Kochi Gothic', 18)
mywindow = boop.BoopWindow(800,600,scene_manager=boop.scene.SceneManager(), config=config)
scene = MyScene(mywindow)
mywindow.scene_manager.add(scene, 'test')

bg = boop.drawables.Backdrop(mywindow, pyglet.image.load('backdrop.jpg',open('Sakuraecho_Alley_Nagano_Japan.jpg','rb')))
scene.add(bg)

scene.add(boop.drawables.DrawWrapper(mywindow, boop.drawtools.draw_gradbox, (0.2, 0.2, 0.9), (0.8, 0.8, 1.0), True, (300, 300), (100, 100)))
scene.add(boop.drawables.DrawWrapper(mywindow, boop.drawtools.draw_gradbox, (0.2, 0.2, 0.5), (0.8, 0.8, 1.0), False, (200, 300), (100, 100)))

scene.add(boop.drawables.DrawWrapper(mywindow, boop.drawtools.draw_circle_annulus, 300, 300, (1.0, 0.0, 0.0)))

ch = boop.drawables.DraggableImage(mywindow, pyglet.image.load('char.png', open('Kemonomimi_rabbit.svg.png','rb')))
ch.setpos(50,50)
scene.add(ch)

scene.add(boop.drawables.DrawWrapper(mywindow, boop.drawtools.draw_polyline, ((random.randint(0, mywindow.width), random.randint(0, mywindow.height)), (random.randint(0, mywindow.width), random.randint(0, mywindow.height)), (random.randint(0, mywindow.width), random.randint(0, mywindow.height))), (1.0, 0.0, 0.0), 10))

label = boop.drawables.Label(mywindow, fnt, u"Kawaii ^.^ かわいい", (220,220))
scene.add(label)

scene.add(TestLine(mywindow))
scene.add(MouseXhair(mywindow))

mywindow.scene_manager.activate('test')

pyglet.app.run()
