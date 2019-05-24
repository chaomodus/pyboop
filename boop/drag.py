import pyglet
import pyglet.font
import pyglet.graphics


class DragMixin(object):
    """This is an abstract base for drag and drop support. For a useful class based on this see
    `boop.drawables.DraggableDrawableMixin`"""

    _drag_dragging = False

    def can_drag(self, state, x, y):
        """This must be overriden to allow dragging to happen."""
        return False

    def start_drag(self, state, x, y):
        """Called before start of drag. Can veto drag by returning False."""
        return True

    def end_drag(self, state, x, y):
        """Calld at end of drag."""
        return True

    def dragging(self, state, x, y):
        return True

    def is_dragging(self):
        """Returns True if the object is being drug."""
        return self._drag_dragging

    def _drag_start(self, state, x, y):
        self._drag_dragging = True
        state.window.dragging_veto = self
        state.window.push_bind_exclusive("on_mouse_drag", self.on_mouse_drag)

    def _drag_stop(self, state, x, y):
        self._drag_dragging = False
        if state.window.dragging_veto is self:
            state.window.dragging_veto = False
        state.window.pop_bind_exclusive("on_mouse_drag", self.on_mouse_drag)

    def on_mouse_drag(self, state, x, y, dx, dy, buttons, modifiers):
        if (
            (buttons & pyglet.window.mouse.LEFT)
            and not self.is_dragging()
            and self.can_drag(state, x, y)
            and not state.window.dragging_veto
        ):
            if self.start_drag(state, x, y):
                self._drag_start(state, x, y)
        elif self.is_dragging():
            if not (buttons & pyglet.window.mouse.LEFT):
                if self.is_dragging():
                    self._drag_stop()
                    self.end_drag(state, x, y)
            else:
                self.dragging(state, x, y)

    def on_mouse_release(self, state, x, y, buttons, modifiers):
        if buttons & pyglet.window.mouse.LEFT and self.is_dragging():
            state.handled = True
            self._drag_stop(state, x, y)
            self.end_drag(state, x, y)
