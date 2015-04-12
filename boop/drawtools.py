import pyglet.graphics
import pyglet.gl as GL
import itertools
import math
tau = math.pi * 2
qtau = math.pi / 2

# NOTE these are inefficient because they recreate the lists each frame
# TODO make static versions of these as Drawables to exploit vertex list objects.
# TODO make static versions that RETURN a VertexList
# TODO use memoization to cache vertex lists even in dynamic (not explicitly static) calls
# TODO make circles take start and stop angles
# TODO make a decorator for gl line drawing routines to make alpha and whatnot work right. (implies wrapper object for static versions)

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

def gl_thickline(startpoint, endpoint, width, color=(1.0,1.0,1.0), z=0.0):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    colspec = get_color_specifier(color, 4)

    rad = width / 2.0

    distancestart = math.sqrt(startpoint[0]**2 + startpoint[1]**2)
    distanceend = math.sqrt(endpoint[0]**2 + endpoint[1]**2)
    if distancestart >  distanceend:
        startpoint, endpoint = endpoint, startpoint

    angle = line_angle(startpoint, endpoint)
    utang = up_tangent(angle)
    dtang = down_tangent(angle)

    coord1 = (endpoint[0] + (rad * math.cos(utang)), endpoint[1] + (rad * math.sin(utang)), z)
    coord2 = (endpoint[0] + (rad * math.cos(dtang)), endpoint[1] + (rad * math.sin(dtang)), z)
    coord3 = (startpoint[0] + (rad * math.cos(dtang)), startpoint[1] + (rad * math.sin(dtang)), z)
    coord4 = (startpoint[0] + (rad * math.cos(utang)), startpoint[1] + (rad * math.sin(utang)), z)

    pyglet.graphics.draw(4, GL.GL_QUADS, ('v3f', coord1+coord2+coord3+coord4), colspec)

    # debug line
    #pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', [float(x) for x in itertools.chain(startpoint, (z,), endpoint, (z,))]), ('c3f', (1.0,1.0,1.0,1.0,1.0,1.0)))


def gl_crosshair(x, y, color=(1.0,1.0,1.0), length=10.0, gap=5.0, z=0.0, angle=0.0):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    x = float(x)
    y = float(y)
    colspec = get_color_specifier(color, 8)
    if angle in (0.0, 90.0, 180.0, 270.0, 360.0):
        pyglet.graphics.draw(8, GL.GL_LINES, ('v3f', (x - (length+gap), y, z, x - gap, y, z,
                                                      x + length+gap, y, z, x + gap, y, z,
                                                      x, y - (length+gap), z, x, y - gap, z,
                                                      x, y + length+gap, z, x, y + gap, z)),
                             colspec)
    else:
        theta1 = angle * (math.pi / 180)
        theta2 = ((angle + 90) % 360) * (math.pi / 180)
        theta3 = ((angle + 180) % 360) * (math.pi / 180)
        theta4 = ((angle + 270) % 360) * (math.pi / 180)
        pyglet.graphics.draw(8, GL.GL_LINES, ('v3f', (x + math.cos(theta1) * gap, y + math.sin(theta1) * gap, z, x + math.cos(theta1) * (gap + length), y + math.sin(theta1) * (gap + length), z,
                                                      x + math.cos(theta2) * gap, y + math.sin(theta2) * gap, z, x + math.cos(theta2) * (gap + length), y + math.sin(theta2) * (gap + length), z,
                                                      x + math.cos(theta3) * gap, y + math.sin(theta3) * gap, z, x + math.cos(theta3) * (gap + length), y + math.sin(theta3) * (gap + length), z,
                                                      x + math.cos(theta4) * gap, y + math.sin(theta4) * gap, z, x + math.cos(theta4) * (gap + length), y + math.sin(theta4) * (gap + length), z)),
                             colspec)


def gl_circle(x, y, color=(1.0,1.0,1.0), radius=10.0, z=0.0, segments=36):
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
    pyglet.graphics.draw(segments, GL.GL_LINE_LOOP, ('v3f', coords),
                         colspec)

def gl_filled_circle(x, y, color=(1.0,1.0,1.0), radius=10.0, z=0.0, segments=36):
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

ARROW_STYLE_PLAIN=0
def gl_arrow(startpoint, endpoint, color=(1.0,1.0,1.0), arrowwidth=15, z=0.0, style=ARROW_STYLE_PLAIN):
    GL.glEnable(GL.GL_LINE_SMOOTH | GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    startpoint = [float(x) for x in startpoint]
    endpoint = [float(x) for x in endpoint]
    angle = line_angle(startpoint, endpoint)
    utang = up_tangent(angle)
    dtang = down_tangent(angle)
    rad = arrowwidth / 2.0
    coord1 = (endpoint[0] + (rad * math.cos(utang)), endpoint[1] + (rad * math.sin(utang)), z)
    coord2 = (endpoint[0] + (rad * math.cos(angle)), endpoint[1] + (rad * math.sin(angle)), z)
    coord3 = (endpoint[0] + (rad * math.cos(dtang)), endpoint[1] + (rad * math.sin(dtang)), z)
    headcol = get_color_specifier(color, 3)
    linecol = get_color_specifier(color, 2)
    pyglet.graphics.draw(3, GL.GL_TRIANGLE_STRIP, ('v3f', coord1+coord2+coord3),headcol)
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', (startpoint[0], startpoint[1], z, endpoint[0], endpoint[1], z)), linecol)
