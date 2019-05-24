from boop.boopwindow import BoopWindow
from boop.fbo import FBO
import pyglet.gl as GL


# FIXME make this work
class PostProcessWindow(BoopWindow):
    def __init__(self, *args, **kwargs):
        BoopWindow.__init__(self, *args, **kwargs)
        self.fbo = FBO(self.width, self.height)
        self.display_rect = ("v2i", (0, 0, self.width, 0, 0, self.height, self.width, self.height))

    def handle_pre_event(self, event_type, *args, **kwargs):
        # This seems like it can't work, at least not with built-in MSAA,
        # cuz pyglet doesn't expose glTexImage2DMultisample et al.
        if event_type == "on_draw":
            self.fbo.attach()
            GL.glViewport(0, 0, self.width, self.height)
            GL.glClearColor(0.0, 0.0, 0.0, 0.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            GL.glPushAttrib(GL.GL_ALL_ATTRIB_BITS)
            GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
            GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glBlendFuncSeparate(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA, GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA)

    def handle_post_event(self, event_type, result, *args, **kwargs):
        if event_type == "on_draw":
            GL.glPopAttrib(GL.GL_ALL_ATTRIB_BITS)
            self.fbo.detach()
            GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
            GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glClearColor(0.0, 0.0, 0.0, 0.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.fbo.get_image_data().blit(0, 0)

    def __del__(self):
        del self.fbo
