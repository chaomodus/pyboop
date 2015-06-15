import pyglet.graphics
import pyglet.gl as GL
import ctypes
import itertools
import math
tau = math.pi * 2
qtau = math.pi / 2
ARROW_STYLE_PLAIN = 0
POLY_CORNER_CHAMFER = 0

# NOTE these are inefficient because they recreate the lists each frame
# TODO make static versions of these as Drawables to exploit vertex list
#      objects.
# TODO make static versions that RETURN a VertexList
# TODO use memoization to cache vertex lists even in dynamic (not explicitly
#      static) calls
# TODO make circles take start and stop angles
# TODO make a decorator for gl line drawing routines to make alpha and whatnot
#      work right. (implies wrapper object for static versions)
#
# TODO add corner mapping for gradbox so that each corner can have
#      a separate color rather than just 2 colors in a range
# TODO make draw_polyline to replace draw_thickline and take width
#      argument. Deal with stitching corners and corner options.
# TODO make draw_polyline_loop as above but loops
# TODO make draw_filled_poly that tesselates area defined by vertex list.


def line_angle(startpoint, endpoint):
    deltax = endpoint[0] - startpoint[0]
    deltay = endpoint[1] - startpoint[1]
    return math.atan2(deltay, deltax)


def up_tangent(angle):
    return (angle + qtau) % tau


def down_tangent(angle):
    return (angle + qtau + math.pi) % tau


def get_color_specifier(basecolor, number):
    color = [float(x) for x in basecolor]
    if len(color) == 3:
        return ('c3d', color * number)
    elif len(color) == 4:
        return ('c4d', color * number)


# this will someday draw nice polylines with corners and whatnot.
# we will also make an effort to guarantee lack of overdraw.
def draw_polyline(vertices, color=(1.0,1.0,1.0), width=1.0, z=0.0, corner_style=POLY_CORNER_CHAMFER):
    lastvert = None
    for vert in vertices:
        if lastvert:
            draw_thickline(lastvert, vert, width, color, z)
        lastvert = vert

def draw_thickline(startpoint, endpoint, width, color=(1.0, 1.0, 1.0), z=0.0):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    colspec = get_color_specifier(color, 4)

    rad = width / 2.0

    distancestart = math.sqrt(startpoint[0]**2 + startpoint[1]**2)
    distanceend = math.sqrt(endpoint[0]**2 + endpoint[1]**2)
    if distancestart > distanceend:
        startpoint, endpoint = endpoint, startpoint

    angle = line_angle(startpoint, endpoint)
    utang = up_tangent(angle)
    dtang = down_tangent(angle)

    coord1 = (endpoint[0] + (rad * math.cos(utang)),
              endpoint[1] + (rad * math.sin(utang)),
              z)
    coord2 = (endpoint[0] + (rad * math.cos(dtang)),
              endpoint[1] + (rad * math.sin(dtang)),
              z)
    coord3 = (startpoint[0] + (rad * math.cos(dtang)),
              startpoint[1] + (rad * math.sin(dtang)),
              z)
    coord4 = (startpoint[0] + (rad * math.cos(utang)),
              startpoint[1] + (rad * math.sin(utang)),
              z)

    pyglet.graphics.draw(4,
                         GL.GL_QUADS,
                         ('v3f', coord1+coord2+coord3+coord4),
                         colspec)


def draw_crosshair(x,
                   y,
                   color=(1.0, 1.0, 1.0),
                   length=10.0,
                   gap=5.0,
                   z=0.0,
                   angle=0.0):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    x = float(x)
    y = float(y)
    colspec = get_color_specifier(color, 8)
    if angle in (0.0, 90.0, 180.0, 270.0, 360.0):
        pyglet.graphics.draw(8, GL.GL_LINES, ('v3f',
                                              (x - (length+gap), y, z,
                                               x - gap, y, z,
                                               x + length+gap, y, z,
                                               x + gap, y, z,
                                               x, y - (length+gap), z,
                                               x, y - gap, z,
                                               x, y + length+gap, z,
                                               x, y + gap, z)),
                             colspec)
    else:
        theta1 = angle * (math.pi / 180)
        theta2 = ((angle + 90) % 360) * (math.pi / 180)
        theta3 = ((angle + 180) % 360) * (math.pi / 180)
        theta4 = ((angle + 270) % 360) * (math.pi / 180)
        pyglet.graphics.draw(8,
                             GL.GL_LINES,
                             ('v3f', (x + math.cos(theta1) * gap,
                                      y + math.sin(theta1) * gap,
                                      z,
                                      x + math.cos(theta1) * (gap + length),
                                      y + math.sin(theta1) * (gap + length),
                                      z,
                                      x + math.cos(theta2) * gap,
                                      y + math.sin(theta2) * gap,
                                      z,
                                      x + math.cos(theta2) * (gap + length),
                                      y + math.sin(theta2) * (gap + length),
                                      z,
                                      x + math.cos(theta3) * gap,
                                      y + math.sin(theta3) * gap,
                                      z, x + math.cos(theta3) * (gap + length),
                                      y + math.sin(theta3) * (gap + length),
                                      z,
                                      x + math.cos(theta4) * gap,
                                      y + math.sin(theta4) * gap,
                                      z,
                                      x + math.cos(theta4) * (gap + length),
                                      y + math.sin(theta4) * (gap + length),
                                      z)),
                             colspec)


def draw_circle(x, y, color=(1.0, 1.0, 1.0), radius=10.0, z=0.0, segments=36):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    x = float(x)
    y = float(y)

    coords = list()
    colspec = get_color_specifier(color, segments)
    for seg in range(0, segments):
        theta = 2.0 * math.pi * seg / segments
        segx = radius * math.cos(theta) + x
        segy = radius * math.sin(theta) + y
        coords.append(segx)
        coords.append(segy)
        coords.append(z)
    pyglet.graphics.draw(segments,
                         GL.GL_LINE_LOOP,
                         ('v3f', coords),
                         colspec)


def draw_filled_circle(x,
                       y,
                       color=(1.0, 1.0, 1.0),
                       radius=10.0,
                       z=0.0,
                       segments=36):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    x = float(x)
    y = float(y)
    colspec = get_color_specifier(color, segments+2)
    coords = [x, y, z]
    for seg in range(0, segments+1):
        theta = 2.0 * math.pi * seg / segments
        segx = radius * math.cos(theta) + x
        segy = radius * math.sin(theta) + y
        coords.append(segx)
        coords.append(segy)
        coords.append(z)
    pyglet.graphics.draw(segments+2, GL.GL_TRIANGLE_FAN, ('v3f', coords),
                         colspec)


def draw_circle_annulus(x,
                        y,
                        color=(1.0, 1.0, 1.0),
                        radius_inner=5.0,
                        radius_outer=10.0,
                        z=0.0,
                        segments=36):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    x = float(x)
    y = float(y)
    coords = []
    for seg in range(0, segments+1):
        theta = 2 * math.pi * seg / segments
        coords.append(x + math.cos(theta) * radius_inner)
        coords.append(y + math.sin(theta) * radius_inner)
        coords.append(z)

        coords.append(x + math.cos(theta) * radius_outer)
        coords.append(y + math.sin(theta) * radius_outer)
        coords.append(z)
    colspec = get_color_specifier(color, len(coords) / 3)
    pyglet.graphics.draw(len(coords) / 3, GL.GL_TRIANGLE_STRIP,
                         ('v3f', coords),
                         colspec)


def draw_arrow(startpoint,
               endpoint,
               color=(1.0, 1.0, 1.0),
               arrowwidth=15,
               z=0.0,
               style=ARROW_STYLE_PLAIN):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    startpoint = [float(x) for x in startpoint]
    endpoint = [float(x) for x in endpoint]
    angle = line_angle(startpoint, endpoint)
    utang = up_tangent(angle)
    dtang = down_tangent(angle)
    rad = arrowwidth / 2.0
    coord1 = (endpoint[0] + (rad * math.cos(utang)),
              endpoint[1] + (rad * math.sin(utang)),
              z)
    coord2 = (endpoint[0] + (rad * math.cos(angle)),
              endpoint[1] + (rad * math.sin(angle)),
              z)
    coord3 = (endpoint[0] +
              (rad * math.cos(dtang)),
              endpoint[1] + (rad * math.sin(dtang)),
              z)
    headcol = get_color_specifier(color, 3)
    linecol = get_color_specifier(color, 2)
    pyglet.graphics.draw(3,
                         GL.GL_TRIANGLE_STRIP,
                         ('v3f', coord1+coord2+coord3),
                         headcol)
    pyglet.graphics.draw(2,
                         GL.GL_LINES,
                         ('v3f',
                          (startpoint[0], startpoint[1], z,
                           endpoint[0], endpoint[1], z)),
                         linecol)


def draw_gradbox(startcolor=(0.0, 0.0, 0.0),
                 endcolor=(0.0, 0.0, 0.0),
                 vertical=True,
                 position=(0, 0),
                 size=(0, 0),
                 z=0.0):
    z = float(z)
    startcoords = [float(x) for x in position]
    endcoords = [float(x + y) for x, y in zip(position, size)]
    if len(startcolor) == 4:
        colspec = 'c4f'
    else:
        colspec = 'c3f'
    if vertical:
        pyglet.graphics.draw(4, GL.GL_QUADS,
                             ('v3f', (startcoords[0],
                                      startcoords[1],
                                      z,
                                      startcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      startcoords[1],
                                      z)),
                             (colspec,
                              startcolor +
                              startcolor +
                              endcolor +
                              endcolor))
    else:
        pyglet.graphics.draw(4, GL.GL_QUADS,
                             ('v3f', (startcoords[0],
                                      startcoords[1],
                                      z,
                                      startcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      startcoords[1],
                                      z)),
                             (colspec,
                              startcolor +
                              endcolor +
                              endcolor +
                              startcolor))


def draw_box(color=(0.0, 0.0, 0.0),
             position=(0, 0),
             size=(0, 0),
             z=0.0,
             width=1):
    z = float(z)
    startcoords = [float(x) for x in position]
    endcoords = [float(x + y) for x, y in zip(position, size)]
    if (not width == 1):
        draw_thickline(startcoords, (startcoords[0], endcoords[1]), width, color)
        draw_thickline((startcoords[0], endcoords[1]), endcoords, width, color)
        draw_thickline(endcoords, (endcoords[0], startcoords[1]), width, color)
        draw_thickline((endcoords[0], startcoords[1]), startcoords, width, color)
    else:
        colspec = get_color_specifier(color, 4)
        pyglet.graphics.draw(4, GL.GL_LINE_LOOP,
                             ('v3f', (startcoords[0],
                                      startcoords[1],
                                      z,
                                      startcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      endcoords[1],
                                      z,
                                      endcoords[0],
                                      startcoords[1],
                                      z)),
                             colspec)
