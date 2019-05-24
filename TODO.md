* Mypy everything
* Tox flake8, black, mypy
* Sphinx docs

* TextArea object.

* Scrollable area object.

* Replace old (removed) event debugging with an integrated event debugging system.

* Introduce standard registry keys that all games share. This is also where we'd
  stick game metadata, player data, etc. There is a stub for the registry, I'd
  like it to be a dict-like object with 'aspects' which are sets of keys that are
  managed downstream, and can be popped and pushed as gamestate changes. This would
  obviously be tied to the scene management stuff very heavily (which needs
  revisiting).

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

* Fix drawtools so that the actual parts that calculate crap are separate
  from the parts that create the batch objects or perform the draw routines
  (so that the calculation can be shared between make* and draw*).

* Make a 1 checkout distribution system to get all of the libraries in one
  place for building binary distributions. (Collect all libraries in one
  place - add pyeuclid as standard).

* Some sort of status / log / display framework for loading and whatnot.
