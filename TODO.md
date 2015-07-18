* Replace old (removed) event debugging with an integrated event debugging system.

* Include a keyboard/mouse mapping system in the Window or Scene object-including
  current state management and impulse emission (indirect keyboard events).

* Include a registry in scene and window objects to record small bits of information
  for sharing between Drawables, etc. Migrate dragging override to this registry.
  Introduce standard registry keys that all games share. This is also where we'd
  stick game metadata, player data, etc.

* Include settings, post-run screen resize support, settings menu.

* Menu/GUI system [perhaps pygui].

* Better resource management. Wrap pyglet's resource system, allow caching etc.
  Indirect resource loading from URLs.

* Integrate cap'n proto for binary save games. Define a definite protocol for
  Scenes and Windows to serialize their children. Gamestate saved in registry
  keys to be serialized too. Offer useful generics for savegames but the ability
  to make a subclass of the schema (or rather, for a custom schema as long as
  some parts of the pyboop schema are included).

* Introduce cap'n proto for network communications. Have a generic key-value
  exchange network standard, with signatures and public key crypto (look
  at NaCL or pycrypto).

* Use a metaclass to track event handlers and register (subscribe) them at
  runtime rather than handling all events. Make it invisible to current
  event infrastructure [eg no user code would change, just everything gets
  faster].

* Implement the numerous TODOs in drawtools and drawables. Biggest is using
  static vertex lists for caching draws - this should allow a huge framerate
  boost in games which use draw routines heavily (Soundwell).

* Make a 1 checkout distribution system to get all of the libraries in one
  place for building binary distributions. (Collect all libraries in one
  place - add pyeuclid as standard).
