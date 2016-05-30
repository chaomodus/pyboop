import euclid

"""
This module has several utilities that don't filt elsewhere.
"""



def point_in_circle(point, circ_center, circ_radius):
    """Check if a specified point is within a circle."""
    pt = euclid.Point2(*point)
    circ = euclid.circle(circ_center, radius=circ_radius)
    return circ.intersect(pt)


def point_in_rectangle(point, rect_bottom_corner, rect_dimensions):
    """Check if a specific point is within a rectangle."""
    rect_top_corner = (rect_bottom_corner[0] + rect_dimensions[0],
                       rect_bottom_corner[1] + rect_dimensions[1])

    return point[0] >= rect_bottom_corner[0] and \
        point[0] <= rect_top_corner[0] and \
        point[1] >= rect_bottom_corner[1] and \
        point[1] <= rect_top_corner[1]

def chunker(seq, size):
    """Chunkify a sequence into `size` length chunks."""
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))
