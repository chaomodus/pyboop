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

    def on_movecamera(self, evt, (vpx, vpy)):
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
    def __init__(self, window, xoffs=0, yoffs=0):
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

        x = 0
        y = 0

        for i in range(1000):
            spr = pyglet.sprite.Sprite(self.tiles[random.randint(0,(12*12) - 1)], batch=self.spritebatch)
            spr.x = x
            spr.y = y
            if (x > 3200):
                x = 0
                y += 32
            x+=32

            self.sprites.append(spr)


    def handle_event(self, window, scene_manager, event_type, *args):
        if event_type == 'on_draw':
            window.clear()
            self.label.draw()
            x = 0
            y = 0
            xoffset, yoffset = scene_manager.get_camera()
            for spr in self.sprites:
                spr.x = x+xoffset
                spr.y = y+yoffset

                if (x > 3200):
                    x = 0
                    y += 32
                x+=32

            self.spritebatch.draw()
        if event_type == 'on_key_press':
            symbol, modifiers = args
            if symbol == pyglet.window.key.UP:
                scene_manager.move_camera(0,32)
            elif symbol == pyglet.window.key.DOWN:
                scene_manager.move_camera(0,-32)
            elif symbol == pyglet.window.key.RIGHT:
                scene_manager.move_camera(32,0)
            elif symbol == pyglet.window.key.LEFT:
                scene_manager.move_camera(-32,0)
            else:
                print symbol
