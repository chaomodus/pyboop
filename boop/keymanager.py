from .component import component
import pyglet.window
import ConfigParser
import io

"""
Manage keyboard input.
"""

def _lookup_binding_value(name):
    """Translate an @'d name into the pyglet value for that name."""
    if '@' in name:
        if name[1:].upper() in pyglet.window.key.__dict__:
            return pyglet.window.key.__dict__[name[1:].upper()]
    print name
    return name

def abstract_load_config(keymanager, reset=False, binddict={}, impulselist=[], watchlist=[]):
    """Implement your own key configuration loader by calling this with a series of lists and dictionaries."""
    if reset:
        keymanager.reset()

    for binding in binddict:
        keymanager.alias(_lookup_binding_value(binding),
                         _lookup_binding_value(binddict[binding]))
        keymanager.track(_lookup_binding_value(binddict[binding]))

    for impulse in impulselist:
        keymanager.impulse(_lookup_binding_value(impulse))

    for watch in watchlist:
        keymanager.track(_lookup_binding_value(watch))
    return keymanager


def load_config(keymanager, reset=False, configfile='', defaultconfig=''):
    """
    Load an INI style config file.


    Recognizes two sections, Options and Bindings. Options can contain
    the keys impulses and watch, which use a CR delimited list of key
    names to indicate keys which are tracked and produce impulses.
    In the Bindings section, each key is interpreted as a key name which
    is aliased to its value.

    Keynames are either strings, or strings starting with an @ symbol
    indicating as predefined key name in Boop such as @F9.
    """
    cf = ConfigParser.SafeConfigParser()
    if defaultconfig:
        cf.readfp(io.BytesIO(defaultconfig))
    cf.read(configfile)

    impulselist = []
    watchlist = []
    bindings = {}
    if cf.has_section('Options'):
        if cf.has_option('Options','impulses'):
            impulselist = cf.get('Options','impulses').split('\n')
        if cf.has_option('Options', 'watch'):
            watchlist = cf.get('Options', 'watch').split('\n')
    if cf.has_section('Bindings'):
        for binding in cf.items('Bindings'):
            bindings[binding[0]] = binding[1]
    return abstract_load_config(keymanager,
                                reset=reset,
                                binddict=bindings,
                                impulselist=impulselist,
                                watchlist=watchlist)


class KeyManager(component.Component):
    """
    This is a component which records up/down state of keyboard and and mouse buttons and prouduces impulses.

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

    The key manager also acts as a dictionary. Accessing the value will return the current key state (or
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
        """Set all key states to "up"."""
        if key is None:
            for key in self.key_states:
                self.key_states[key] = False
        else:
            self.key_states[key] = False

    def state(self, key):
        """Get the state of a particlar key."""
        if key in self.key_states:
            return self.key_states[key]
        return None

    def alias(self, key, value):
        """Assign an alias to a particular key."""
        self.key_aliases[key] = value

    def delalias(self, key):
        """Remove a key alias."""
        if key in self.key_aliases:
            del self.key_aliases[key]

    def track(self, key):
        """Tell the keyboard manager to start tracking the states of a particular key."""
        self.key_trackstates.add(key)

    def deltrack(self, key):
        """Tell the keyboard manager to stop tracking the states of a particular key."""
        self.key_trackstates.remove(key)
        if key in self.key_states:
            del self.key_states[key]

    def impulse(self, key):
        """Ask for impulses to be emitted for a specific key."""
        self.key_impulses.add(key)

    def delimpulse(self, key):
        """Stop emitting impulses for a specific key."""
        self.key_impulses.remove(key)

    def on_key_press(self, state, startkey, modifiers):
        """Internal keypress handler."""
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
        """Internal keyrelease handler."""
        if startkey in self.key_aliases:
            key = self.key_aliases[startkey]
        else:
            key = startkey

        if key in self.key_states:
            self.key_states[key] = False

        if key != startkey and self.reemit:
            state.window.dispatch_event('on_key_release', key, modifiers)
