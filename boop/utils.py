import euclid


def point_in_circle(point, circ_center, circ_radius):
    pt = euclid.Point2(*point)
    circ = euclid.circle(circ_center, radius=circ_radius)
    return circ.intersect(pt)


def point_in_rectangle(point, rect_bottom_corner, rect_dimensions):
    rect_top_corner = (rect_bottom_corner[0] + rect_dimensions[0],
                       rect_bottom_corner[1] + rect_dimensions[1])

    return point[0] >= rect_bottom_corner[0] and \
        point[0] <= rect_top_corner[0] and \
        point[1] >= rect_bottom_corner[1] and \
        point[1] <= rect_top_corner[1]

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
