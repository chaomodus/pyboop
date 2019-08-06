# -*- coding: utf-8 -*-
# NOTE! THis file will change frequently as features are developed and used.
# Examples of developed frameworks and uses will be spun off into separate files as needed.
# Current use: tilegrid development
#
import sys
sys.path.append('../')
import pyglet
from boop.boopwindow import BoopWindow
import boop
import boop.scenemanager
from boop.scene import Scene
from boop.drawables import Drawable, Clear
from boop.tilegrid import Tilegrid
import boop.drawtools
from boop.keymanager import KeyManager
import math
import random

from collections import OrderedDict

mymap = ['.........................',
         '.........................',
         '.................####....',
         '.................#..#....',
         '.................#..+....',
         '.................####....',
         '.......#####.............',
         '.......#...#.............',
         '.......#...+.............',
         '.......#...#.............',
         '.......#####.............',
         '.........................',
         '............###+#........',
         '............#...#........',
         '.#####......#...#........',
         '.#...+......#...#........',
         '.#####......#####........',
         '.........................',
]

class MyMap(Tilegrid):
    adds = {
        pyglet.window.key.UP: (0, 1),
        pyglet.window.key.DOWN: (0, -1),
        pyglet.window.key.LEFT: (-1, 0),
        pyglet.window.key.RIGHT: (1, 0),
    }

    def on_impulse(self, state, key):
        if key in self.adds:
            adds = self.adds[key]
            self.move_camera(*adds)
            return True
        return False

    def move_camera(self, x, y):
        xsiz, ysiz = self.get_tile_size()
        self.setpos(self.position[0] + (x * -1 * xsiz), self.position[1] + (y * -1 * ysiz))

config = pyglet.gl.Config()
mywindow = BoopWindow(1536, 864, scene_manager=boop.scenemanager.SceneManager(), config=config)
keymanager = KeyManager(False)
keymanager.impulse(pyglet.window.key.UP)
keymanager.impulse(pyglet.window.key.DOWN)
keymanager.impulse(pyglet.window.key.LEFT)
keymanager.impulse(pyglet.window.key.RIGHT)
mywindow._registry['keymanager'] = keymanager
scene = Scene(mywindow)
scene.add(Clear(mywindow))
scene.add(keymanager)
mywindow.scene_manager.add(scene, 'test')

mytiles = MyMap(mywindow, 32, 32, 1)
mytiles.tilegrid[0] = mymap
mytiles.load_tile('#', 'rock.png')
mytiles.load_tile('+', 'door.png')

mytiles.setpos(10,10)
mytiles.setsize(x=1520, y=1152)
scene.add(mytiles)
scene.add(boop.drawables.DrawWrapper(mywindow, boop.drawtools.draw_circle_annulus, -300, -300, (1.0, 0.0, 0.0)))

mywindow.scene_manager.activate('test')
mywindow.activate()
mywindow.switch_to()
pyglet.app.run()
