# boop specific events
boop_events = ['on_tick',
               'on_select',
               'on_activate',
               'on_decativate',
               'on_movecamera',
               'on_mouseover',
               'on_impulse', ]


class EventStateHolder(object):
    """This object is meant to hold event state. It is passed to ever event handler when the event triggers."""
    # Any client may indicate that they've handled the event by setting to True
    handled = False
    # Set by the window when the event is issued
    window = None
    registry = None
    # Set by the scene manager when the event is issued.
    scene_manager = None
    # Set by the scene
    scene = None
    # set by ComponentHost when it passes the event (immediate parent)
    container = None
