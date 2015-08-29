from .component import component
import pyglet.window

class KeyManager(component.Component):
    """This is a component which records up/down state of keyboard and and mouse buttons and prouduces impulses.

    Add this to your  Window or Scene to manage keys, aliasing keys, track keys, and create secondary handlers
    for keys.

    Order of operations:
      1. Assign current key based on aliases.
      2. Emit impulse event for key up / down.
      3. Update key_states
      4. Re-emit event if it was alias indirected. This can create an infinite looop if there are loops in
         the aliasing.

    Note that aliases can be aribtrary values, so they can be used to assign non-overlapping values for
    keys, for, for example, creating key mappings to arbitrary end points.

    The key manager also acts as a dictionry. Accessing the value will return the current key state (or
    up if it is an untracked key).

    Impulses are basically second-order keyboard events that only emit on key down.
    """

    def __init__(self, reemit=True):
        component.Component.__init__(self)

        self.key_aliases = {}
        self.key_impulses = set()
        self.key_trackstates = set()
        self.key_states = {}
        self.reemit = reemit

    def reset(self, key=None):
        if key is None:
            for key in self.key_states:
                self.key_states[key] = False
        else:
            self.key_states[key] = False

    def state(self, key):
        if key in self.key_states:
            return self.key_states[key]
        return None

    def alias(self, key, value):
        """Assign an alias to a particular key."""
        self.key_aliases[key] = value

    def delalias(self, key):
        if key in self.key_aliases:
            del self.key_aliases[key]

    def track(self, key):
        self.key_trackstates.add(key)

    def deltrack(self, key):
        self.key_trackstates.remove(key)
        if key in self.key_states:
            del self.key_states[key]

    def impulse(self, key):
        self.key_impulses.add(key)

    def delimpulse(self, key):
        self.key_impulses.remove(key)

    def on_key_press(self, state, startkey, modifiers):
        if startkey in self.key_aliases:
            key = self.key_aliases[startkey]
        else:
            key = startkey

        if key in self.key_impulses:
            state.window.dispatch_event('on_impulse', key)

        if key in self.key_trackstates:
            self.key_states[key] = True

        if key != startkey and self.reemit:
            state.window.dispatch_event('on_key_press', key, modifiers)

    def on_key_release(self, state, startkey, modifiers):
        if startkey in self.key_aliases:
            key = self.key_aliases[startkey]
        else:
            key = startkey

        if key in self.key_states:
            self.key_states[key] = False

        if key != startkey and self.reemit:
            state.window.dispatch_event('on_key_release', key, modifiers)
