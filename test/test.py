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
import random
import math

# menu
#  pages
#   items -> events
# menu itemsz need to be able to eb generated, and rendered with arbitrary code.
# menu items define a particular part of teh screen (queriable)
# menu items have a selected and unselected state
# menu items handle key presses and mouse events
# define special api for them to change focus/page?
# menu items should be just this much more than a drawable object with focus control

#abc
class MenuItem(Drawable):
    def __init__(self, display):
        Drawable.__init__(self, display)

    def on_select(self, *args):
        return None

    def on_deselect(self, *args):
        return None

    def on_activate(self, *args):
        return None

    def on_mouseover(self, *args):
        return None

class TextMenuItem(MenuItem):
    pass

class ToggleMenuItem(TextMenuItem):
    pass

class SelectMenuItem(TextMenuItem):
    pass

class IconMenuItem(MenuItem):
    pass

class MenuScene(boop.scene.Scene):
    def __init__(self, window, menudefs=None):
        boop.scene.Scene.__init__(self, window)

class MyScene(boop.scene.Scene):
    def __init__(self, window):
        boop.scene.Scene.__init__(self, window)
        self.components.append(boop.drawables.Clear(window))

class TestLine(Drawable):
    def render(self, window):
        x = 100
        y = 500
        for i in range(0, 100, 10):
            boop.drawtools.gl_thickline((x, y), (x + (100 * math.cos(math.pi * 2 * (i / 100.0))), y + (100 * math.sin(math.pi * 2 * (i / 100.0)))), i / 10, color=(1.0 - i / 100.0, i / 100.0, i / 100.0, 1.0))
        x = (window.width / 2) + 200
        y = (window.height / 2) + 200
        for i in range(0, 100, 10):
            boop.drawtools.gl_arrow((x, y), (x + (100 * math.cos(math.pi * 2 * (i / 100.0))), y + (100 * math.sin(math.pi * 2 * (i / 100.0)))), color=(i / 100.0, i / 100.0, 1.0 - i / 100.0, 1.0))

fnt = pyglet.font.load('Kochi Gothic', 18)

mywindow = boop.BoopWindow(800,600,scene_manager=boop.scene.SceneManager())
scene = MyScene(mywindow)
mywindow.scene_manager.add(scene, 'test')

bg = boop.drawables.Backdrop(mywindow, pyglet.image.load('backdrop.jpg',open('Sakuraecho_Alley_Nagano_Japan.jpg','rb')))
scene.add(bg)

scene.add(boop.drawables.GradBox(mywindow, (0.2, 0.2, 0.9), (0.8,0.8,1.0), True, (300, 300), (100, 100)))
scene.add(boop.drawables.GradBox(mywindow, (0.2, 0.2, 0.5), (0.8,0.8,1.0), False, (200, 300), (100, 100)))

ch = boop.drawables.Image(mywindow, pyglet.image.load('char.png', open('Kemonomimi_rabbit.svg.png','rb')))
scene.add(ch)

label = boop.drawables.Label(mywindow, fnt, u"Kawaii ^.^ かわいい", (220,220))
#label = boop.drawables.Label(mywindow, fnt, "Kawaii ^.^", (220,220))
scene.add(label)

scene.add(TestLine(mywindow))

mywindow.scene_manager.activate('test')

pyglet.app.run()
