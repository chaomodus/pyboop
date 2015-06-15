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
from boop.drawables import Drawable, DrawWrapper
import boop.drawtools
import math
import itertools

# menu scene
# (frame drawable)
#  page scene (optional)
#   item drawable (events)
#
# menu itemsz need to be able to eb generated, and rendered with arbitrary code.
# menu items define a particular part of teh screen (queriable)
# menu items have a selected and unselected state
# menu items handle key presses and mouse events
# define special api for them to change focus/page?
# menu items should be just this much more than a drawable object with focus control

class MenuItem(Drawable):
    def __init__(self, display):
        Drawable.__init__(self, display)
        self.selected = False

    def on_select(self, state, *args):
        self.selected = True
        return None

    def on_deselect(self, state, *args):
        self.selected = False
        return None

    def on_activate(self, state, *args):
        return None

    def on_mouseover(self, state, *args):
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
    # per page: menudefs = {'menupage':[menuitems, ...]}
    # page '' is 1st or default page
    # global: statics = [drawables, ...]
    def __init__(self, window, default_font, statics=[], menudefs={}):
        boop.scene.Scene.__init__(self, window)
        self.statics = statics
        self.menudefs = menudefs
        self.pagestack = list()
        self.page = ''
        if '' in menudefs:
            self.set_page('')
        else:
            self.components = list(self.statics)

    def add(self, component):
        self.statics.append(component)
        self._do_set_page(self, self.page)

    def _do_set_page(self, page):
        if page == '' and not self.menudefs:
            self.components = list(self.statics)
        else:
            self.page = page
            self.components = itertools.chain(self.statics, self.menudefs[page]['statics'], self.menudefs[page]['menuitems'])

    def set_page(self, page):
        self.pagestack = list()
        self._do_set_page(page)

    def push_page(self, newpage):
        self.pagestack.append(self.page)
        self._do_set_page(newpage)

    def pop_page(self):
        pg = self.pagestack.pop()
        self._do_set_page(pg)

fnt = pyglet.font.load('Kochi Gothic', 18)
mywindow = boop.BoopWindow(800,600,scene_manager=boop.scene.SceneManager())
scene = boop.scene.Scene(mywindow)
mywindow.scene_manager.add(scene, 'backdrop')

bg = boop.drawables.Backdrop(mywindow, pyglet.image.load('backdrop.jpg',open('Sakuraecho_Alley_Nagano_Japan.jpg','rb')))
scene.add(bg)
ch = boop.drawables.Image(mywindow, pyglet.image.load('char.png', open('Kemonomimi_rabbit.svg.png','rb')))
scene.add(ch)

label = boop.drawables.Label(mywindow, fnt, u"Kawaii ^.^ かわいい", (290,mywindow.height-250))
#scene.add(label)

backdrop = DrawWrapper(mywindow, boop.drawtools.draw_gradbox, startcolor=(0.3,0.3,0.6), endcolor=(0.6,0.6,0.8), position=(250,100), size=(mywindow.width / 1.75, mywindow.height /2))

menuscene = MenuScene(mywindow, fnt, statics=[backdrop,label])
mywindow.scene_manager.add(menuscene, 'menutest')

mywindow.scene_manager.activate('backdrop')
mywindow.scene_manager.activate('menutest')


pyglet.app.run()
