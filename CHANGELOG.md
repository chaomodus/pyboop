# ChangeLog

## [Unreleased] [Unreleased]

Batch drawables. Better keyboard management.

### Added
- Added keyboardmanager, and mechanics for managing key bindings, aliases and
  second-order keyboard events.
- Added temporary _registry item to BoopWindow to act as the registry until
  we formalize it.

### Changes
- Changed make_* routines to return a special BatchDraw obect which implements
  parts of the Drawable protocol (and is a full drawable). It could conceivably
  implement the entire protocol.
- Make BoopWindow call its own handler so that its direct children can recieve events.

## [0.0a9] - 2015-07-21 - chaomodus

Vertex lists, oh my!

### Added
- Added make_* versions of routines in drawtools. These create draw batches
  using Pyglet's built-in batching system. The accept a batch argument (which
  is optional, a new batch is created if one isn't passed), and return a batch
  with the draws in it. Batches can be drawn using the .draw routine.
- Stub for registry, and notes in TODO about it. Registry will be a place for
  shared data between components, status information and game state. Registry
  will be passed with EventState object.
- Added ClockDisplay which wraps the ClockDisplay in Pyglet in a Drawable.
- Added impulse event type for future key binding fun.

### Changes
- Underscored some variables on Window to indicate that they are not for downstream
  consumption.

### Notes
- Started keeping a change log, with differences from 0.0a8. Changelog entries
  will summarize changes since last release. Releases in the alpha series occur
  approximately every commit until 1.0.0.
- May have come up with a solution for the call semantics on the exclusive handler
  mechanism.
