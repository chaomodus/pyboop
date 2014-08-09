import pyglet
import boop
import boop.component
import boop.scene
import random

class StageLoader(object):
    def __init__(self, stagedict):
        self.definition = stagedict
        self.stage = None

    def __call__(self):

        return self.stage

    def force_reload(self):
        self.stage = None

class Layer(boop.component.Component):
    # contains exactly one layer of a stage.
    def __init__(self, x, y, index, scroll_offset=(0,0)):
        self.x = x
        self.y = y
        self.index = index
        self.scroll_offset = scroll_offset
        self.vpx = 0
        self.vpy = 0

    def get_effective_viewport(self):
        # do math here
        return self.vpx, self.vpy

    def on_setviewport(self, evt, vpx, vpy):
        self.vpx = vpx
        self.vpy = vpy

class BackgroundLayer(Layer):
    # contains a single large image that is tiled and scrolled
    pass

class GridLayer(Layer):
    # contains a list of tiles at fixed positions with a collision mask.
    pass

class Stage(boop.component.Component):
    # contains map, actors, particles, etc.
    pass

class CutScene(boop.scene.Scene):
    def __init__(self, data=None, options={}):
        self.csdata = csdata
        self.csoptions = csoptions
        self.csstack = list()
        boop.scene.Scene.__init__(self)

class IntercutScene(CutScene):
    # acts like a cutscene and like a actedscene except doesn't pass all events to the actors (control events andh such)
    # would share the Stage with the ActedScene so that intercuts could be made
    def __init__(self, data=None, options={}):
        CutScene.__init__(self, data, options)


class TestScene(boop.scene.Scene):
    def __init__(self, window):
        boop.scene.Scene.__init__(self)
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=window.width//2, y=window.height//2,
                                       anchor_x='center', anchor_y='center')
        tiles_image = pyglet.image.load('test/intbuilding7a_0.png')
        self.tiles = pyglet.image.ImageGrid(tiles_image, 12,12)
        self.sprites = list()
        self.spritebatch = pyglet.graphics.Batch()
        self.xoffset = 300
        self.yoffset = 300
        x = 0
        y = 0
        for i in range(10000):
            spr = pyglet.sprite.Sprite(self.tiles[random.randint(0,(12*12) - 1)], batch=self.spritebatch)
            self.sprites.append(spr)

            spr.x = x + self.xoffset
            spr.y = y + self.yoffset
            if (x > 32000):
                x = 0
                y += 32
            x+=32

    def handle_event(self, window, scene_manager, event_type, *args):
        if event_type == 'on_draw':
            window.clear()
            self.label.draw()
            x = 0
            y = 0
            for spr in self.sprites:
                spr.x = x+self.xoffset
                spr.y = y+self.yoffset

                if (x > 32000):
                    x = 0
                    y += 32
                x+=32

            self.spritebatch.draw()
        if event_type == 'on_key_press':
            symbol, modifiers = args
            if symbol == pyglet.window.key.UP:
                self.yoffset += 32
            elif symbol == pyglet.window.key.DOWN:
                self.yoffset -= 32
            elif symbol == pyglet.window.key.RIGHT:
                self.xoffset += 32
            elif symbol == pyglet.window.key.LEFT:
                self.xoffset -= 32
            else:
                print symbol

mywindow = boop.BoopWindow(1300,700,scene_manager=boop.scene.SceneManager())
mywindow.scene_manager.scenes['test'] = TestScene(mywindow)
mywindow.scene_manager.activate_scene('test')

pyglet.app.run()
