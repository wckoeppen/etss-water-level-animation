#!/user/bin/env python
# coding=utf-8

import math

def extend_extent(extent, fig_size):
    """Extend map extents to fill a given figure aspect.

    Parameters
    ----------
    extent: (float, float, float, float)
        Tuple of floats representing the required extent
        (x0, x1, y0, y1)

    fig_size : (float, float)
        [description]

    Returns
    -------
    (float, float, float, float)
        Tuple of floats representing the new, extended extents
        (x0, x1, y0, y1)
    """

    # width:height
    fig_aspect = fig_size[0] / fig_size[1]
    extent_width = extent[1] - extent[0]
    extent_height = extent[3] - extent[2]
    extent_center_lon = extent_width / 2. + extent[0]
    extent_center_lat = extent_height / 2. + extent[2]
    extent_aspect = extent_width / extent_height

    # Scale factor for mercator projection
    scale_factor = 1. / math.cos(math.radians(extent_center_lat))
    scaled_extent_width = extent_width * scale_factor

    # if we need to fill in a figure wider than the map
    if fig_aspect > (extent_aspect * scale_factor):
        r_extent_width = extent_width * (fig_aspect/extent_aspect) * scale_factor

        r_minlon = extent_center_lon - r_extent_width/2.
        r_maxlon = extent_center_lon + r_extent_width/2.

        r_extent = (r_minlon, r_maxlon, extent[2], extent[3])

        # if we need to fill in a figure taller than the map
        print("extent_w: ", extent_width)
        print("extent_h: ", extent_height)
        print("scale: ", scale_factor)
        print("scaled extent width: ", scaled_extent_width)
        print("fig aspect: ", fig_aspect)
        print("extent aspect: ", extent_aspect)
        print("recalculated_w ", r_maxlon-r_minlon)
        print(extent_center_lon)
        print(r_extent_width)

    else:
        r_extent = extent

    return r_extent
    