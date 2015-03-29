import pyglet.graphics
import pyglet.gl as GL
import itertools
import math
tau = math.pi * 2
qtau = math.pi / 2

def line_angle(startpoint, endpoint):
    deltax = startpoint[0] - endpoint[0]
    deltay = startpoint[1] - endpoint[1]

    return math.atan2(deltax, deltay)

def up_tangent(angle):
    return (angle + qtau) % tau

def down_tangent(angle):
    return (angle - qtau) % tau

def get_color_specifier(basecolor, number):
    color = [float(x) for x in basecolor]
    if len(color) == 3:
        return ('c3f', color * number)
    elif len(color) == 4:
        return ('c4f', color * number)

def gl_thickline(startpoint, endpoint, width, color, z=0.0):
    # doesn't work dunno why
    rad = width / 2.0

    distancestart = math.sqrt(startpoint[0]**2 + startpoint[1]**2)
    distanceend = math.sqrt(endpoint[0]**2 + endpoint[1]**2)
    if distancestart >  distanceend:
        startpoint, endpoint = endpoint, startpoint

    # debug line
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', [float(x) for x in itertools.chain(startpoint, (z,), endpoint, (z,))]), ('c3f', (1.0,1.0,1.0,1.0,1.0,1.0)))

    angle = line_angle(startpoint, endpoint)
    utang = up_tangent(angle)
    dtang = down_tangent(angle)
    coord1 = (startpoint[0] + rad * math.sin(utang), startpoint[0] + rad * math.cos(utang), z)
    coord2 = (startpoint[0] + rad * math.sin(dtang), startpoint[0] + rad * math.cos(dtang), z)
    coord3 = (endpoint[0] + rad * math.sin(utang), endpoint[0] + rad * math.cos(utang), z)
    coord4 = (endpoint[0] + rad * math.sin(dtang), endpoint[0] + rad * math.cos(dtang), z)

    pyglet.graphics.draw(6, GL.GL_QUADS, ('v3f', coord1+coord1+coord2+coord3+coord4+coord4), ('c3f', color*6))

def gl_crosshair(x, y, color=(1.0,1.0,1.0), length=10.0, gap=5.0, z=0.0):
    x = float(x)
    y = float(y)
    colspec = get_color_specifier(color, 2)
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', (x - (length+gap), y, z, x - gap, y, z)),
                         colspec)
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', (x + length+gap, y, z, x + gap, y, z)),
                         colspec)
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', (x, y - (length+gap), z, x, y - gap, z)),
                         colspec)
    pyglet.graphics.draw(2, GL.GL_LINES, ('v3f', (x, y + length+gap, z, x, y + gap, z)),
                         colspec)

def gl_circle(x, y, color=(1.0,1.0,1.0), radius=10.0, z=0.0, segments=36):
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
