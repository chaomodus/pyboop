# ChangeLog

## [0.0a16 WIP] - chaomodus

Only Python3 supported now, changes to make that the case.


## [0.0a14] - chamodus

Cleanups and minor fixes.


## Fixes
- Fixed typo in drawables.DrawWrapper.
- Indirect window fixes
- Cleaned up BoopWindow imports and style.
- Enhanced fade mixin to allow for variable speed.

## [0.0a12] - 2016-05-30 - chaomodus

Improvements to drawables.Image. Drawable improvements. Other fixes and improvements.

### Changes
- Major documentation pass. Most classes, modules and methods should be
  at least basically documented now.
- Added scale support to Image. Removed extraneous methods.
- Moved repositioning code to render_at in Drawable to ease drawing the
  same object at several locations. render now calls render_at with
  the drawable's position.
- Drawable does a little more in the base class as far as size and position.
- Image now falls back on Drawable for much of its functions. Now supports
  setscale which sets the scale on the sprite.
- LayeredDict has had numerous minor changes and rationalizations.

## [0.0a11] - 2016-01-24 - chaomodus

Make batches really a lot faster if moving. Enhance keyboard manager.

### Added
- Keyboard manager now has functions in the module to load an INI style config
  file to setup keyboard settings. Useful for use-editable keyboard maps.

### Changes
- Use translation on batches instead of changing vertexes every time the batch is moved;
  this should make drawing batches exceptionally faster.
- As part of above, rejigger Drawable API. Now render(self,window) on the drawable is
  expected to do any viewport manipulation. do_render takes the place of the previous
  render command (positions viewport by default).

## [0.0a10] - 2015-10-01 - chaomodus

Batch drawables. Better keyboard management. LayeredDict.

### Added
- Added keymanager, and mechanics for managing key bindings, aliases and
  second-order keyboard events.
- Added a LayeredDict object for storing registry like data.
- Added a _registry attribute to boopwindow. Access from the event state as the
  registry member.

### Changes
- Changed make_* routines to return a special BatchDraw obect which implements
  parts of the Drawable protocol (and is a full drawable). It could conceivably
  implement the entire protocol.
- Make BoopWindow call its own handler so that its direct children can recieve events.
- Separate drawable into its own subcomponent.


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
