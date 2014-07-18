# pyBOOP!

2d Love

- Actors
-- Behaviors
-- Animations
-- Gravity
- Scenes
-- Levels
-- Maps
-- Cutscenes
- Collisions
- Projectiles
- Menu system
- Particle system


Scene(object)
  mainloop
  event_handlers

ActedScene(Scene)
  actors[] (actors)
  particles(?)
  map[] (tiles, mask)
  objects[] (actors)
  musiccues[] (player_position, musiccue)

MenuScene(Scene)
  pages[]
    items[]

MenuItem(object)

CutScene(Scene)
  events[]

Component(object)

ComponentHost(object)
  components[]

Actor(ComponentHost)
  PhysicsComp
  InputComp
  DrawComp
  CollideComp
  LoopComp
  SoundComp

CutSceneEvent(ComponentHost)
  ImageComp
  LoopComp
  TextComp
  SFXComp
  MusicComp


# Event Propogation
(Scene)ACS.handle_thing
  Actor1.handle_thing
    Component1.handle_thing
    Component2.handle_thing
    ...
    ComponentN.handle_thing
  Actor2.handle_thing
  ...
  ActorN.handle_thing
