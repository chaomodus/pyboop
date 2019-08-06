from collections import OrderedDict
from typing import Dict

from pyglet.image import Texture, TextureRegion
import pyglet.resource

from .drawable import Drawable
from .batchdraw import BatchDraw

# Define a tilemap in terms of keys within an array of images
# 1 Define tilemap layers
# 2 load images that match tile names
# 3 Call _assemble_image: the tilegrid is iterated, and based on the tilesize, the internal Texture is updated with the
#   contents of the tiles{} dictionary blitted into it. It is then ready to draw.
# 4 .draw()

class Tilegrid(Drawable):
    def __init__(self, window, tilesize_x, tilesize_y, mult=1):
        Drawable.__init__(self, window)
        self._tilegrid = OrderedDict()
        self._tiles = {}
        self._origin = (0,0)
        self._destination = (0,0)
        self._image = None
        self._tile_x = tilesize_x
        self._tile_y = tilesize_y
        self._mult = mult


    @property
    def tilegrid(self):
        # return thte internal timemap layer
        return self._tilegrid

    def tilegrid_layer(self, name):
        # Return the named layer from the tilegrid
        return self._tilegrid[name]

    def add_tile(self, key, image):
        # Add a tile to the tiles list
        self._tiles[key] = image

    def load_tile(self, key, path):
        img = pyglet.resource.image(path)
        self._tiles[key] = img

    def get_extents(self):
        # Return the size of the tile map in tiles
        maxwidth = 0
        maxheight = 0
        for layer in self._tilegrid:
            height = 0
            for row in self._tilegrid[layer]:
                height += 1
                if len(row) > maxwidth:
                    maxwidth = len(row)
            if height > maxheight:
                maxheight = height
        return (maxwidth, maxheight)

    def set_viewport(self, origin, destination):
        # Set the origin, destination of the viewport we should render
        self._origin = origin
        self._destination = destination

    def get_viewport(self):
        # Return the origin, destination of the view port
        return (self._origin, self._destination)

    def assemble_image(self):
        # Assemble tilegrid into an internal image
        pass

    def _update_tile(self,  tilex, tiley, layer, name):
        # Update one tile in the internal image
        pass

    @property
    def image(self):
        # Return the renderable image based on the viewport
        pass

    def getsize(self):
        ext_x, ext_y = self.get_extents()
        return (self._mult * ext_x * self._tile_x, self._mult * ext_y * self._tile_y)

    def get_tile_size(self):
        return (self._mult * self._tile_x, self._mult * self._tile_y)

    def do_render(self, window):
        ext_x, ext_y = self.get_extents()
        siz_x, siz_y = self.getsize()
        target_x = (siz_x / ext_x)
        target_y = (siz_y / ext_y)
        ratio = self._tile_x / target_x
        for layer in self._tilegrid:
            posy = 0
            for row in reversed(self._tilegrid[layer]):
                posx = 0
                for tile in row:
                    if tile in self._tiles:
                        self._tiles[tile].width = target_x
                        self._tiles[tile].height = target_y
                        self._tiles[tile].blit(posx, posy)
                    posx += target_x
                posy += target_y
