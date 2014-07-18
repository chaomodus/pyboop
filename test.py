
import pyglet
import boop
import boop.scene



class CutScene(boop.scene.Scene):
    def __init__(self, data=None, options={}):
        self.csdata = csdata
        self.csoptions = csoptions
        boop.scene.Scene.__init__(self)


class TestScene(boop.scene.Scene):
    def __init__(self, window):
        boop.scene.Scene.__init__(self)
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=window.width//2, y=window.height//2,
                                       anchor_x='center', anchor_y='center')

    def handle_event(self, window, scene_manager, event_type, *args):
        if event_type == 'on_draw':
            window.clear()
            self.label.draw()



mywindow = boop.BoopWindow(scene_manager=boop.scene.SceneManager())
mywindow.scene_manager.scenes['test'] = TestScene(mywindow)
mywindow.scene_manager.activate_scene('test')


pyglet.app.run()
