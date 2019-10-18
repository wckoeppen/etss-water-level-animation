#!/user/bin/env python
# coding=utf-8

import io
import math
import pickle

import cartopy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cmocean import cm
from PIL import Image


class ResolutionValueError(ValueError):
    pass


def get_resolution(arg):
    """Handle the resolution argument."""
    if isinstance(arg, tuple):
        return arg
    if isinstance(arg, str):
        if arg == "1080p":
            return (1920, 1080)
        if arg == "720p":
            return (1080, 720)
        else:
            # I feel like this isn't the correct error to raise
            raise ResolutionValueError(
                "Valid inputs are '1080p', "
                + "'720p', or a two-element tuple (width, height)."
            )


def resolution_to_figsize(_input_tuple, dpi=72):
    """Convert pixel resolution to inches for input into matplotlib
    figsize."""

    width_px = _input_tuple[0]
    height_px = _input_tuple[1]

    width_inch = width_px / dpi
    height_inch = height_px / dpi

    return (width_inch, height_inch)


def serialize_to_buffer(in_figure_object, dpi=72):
    """Write the matplotlib figure object to a PNG in a buffer."""
    out_buffer = io.BytesIO()
    in_figure_object.savefig(out_buffer, dpi=dpi, format="PNG")
    out_image = Image.open(out_buffer)

    return out_image


# def serialize_to_pickle(in_figure_object):
#     out_buffer = io.BytesIO()
#     cloudpickle.dump(in_figure_object, out_buffer)

#     return out_buffer


def make_basemap(limit=0, extent=(170, 255, 40, 76), resolution="1080p",
                 enforce_extent=False, free_aspect=False):
    """
    Return a basemap image (PNG) with a coastline and rivers.

    Parameters
    ----------
    extent: (float, float, float, float), default:(170, 255, 40, 76)
        Tuple of floats representing the required extent
        (x0, x1, y0, y1)

    limit: integer, default: 0
        The limits of the legend, which should match the
        gridded data

    resolution: (float, float), "1080p", "720p", default:"1080p"
        A tuple dictating the width and height of the output. In
        addition, some strings are accepted. "1080p" is an alias
        for (1920, 1080), and "720p" is aliased to (1080, 720).
        
    free_aspect: bool, default:False
        By default, the aspect ratio of the output is dictated by the
        provided resolution. E.g., if 1080p (1920px x 1080px) is
        provided, the aspect ratio of the output will be 16:9. If
        a free aspect ratio of the output is preferred (e.g., in
        conjunction with enforce_extent), then only the first value
        in the provided resolution will be used for the figure width,
        and the figure height will be inferred from the extent.
    
    enforce_extent: bool, default:False
        By default, the provided extent is treated as a minimum, and
        it will be expanded to fill the aspect ratio of the output
        resolution. Set this parameter to True if you prefer to have
        exact map bounds and use white space to fill the remainder.
    
    
    Returns
    -------
    PNG
        A png image serialized by this function.
    """
    plate_crs = cartopy.crs.PlateCarree()
    merc_crs = cartopy.crs.Mercator(central_longitude=210)

    dpi = 72
    land_color = "#fcfcfc"
    coast_color = "#b1b1b1"
    # ocean_color = "#d7dfe0"
    # box_alpha = 0.7
    # annotation_spacing = 0.2
    cmap = cm.balance

    out_resolution = get_resolution(resolution)
    fig_size = resolution_to_figsize(out_resolution)

    fig = plt.figure(dpi = dpi, figsize = (fig_size[0], fig_size[1]))
    ax = fig.add_axes([0, 0, 1, 1], projection = merc_crs)
    ax.outline_patch.set_visible(False)

    ### Contextual Map Elements ###
    land_10m = cartopy.feature.NaturalEarthFeature(
        "physical", "land", "10m", edgecolor=coast_color, facecolor=land_color
    )
    ax.add_feature(land_10m)

    rivers = cartopy.feature.NaturalEarthFeature(
        "physical",
        "rivers_lake_centerlines",
        "10m",
        edgecolor="#66a0b8",
        facecolor="none",
    )
    ax.add_feature(rivers, alpha=0.2)

    ax.set_extent(extent, crs=plate_crs)

    ### Legend ###
    # if not limit:
    #     limit = math.ceil(np.max(np.abs(surge_image)))

    vmin = -limit
    vmax = limit

    ### ETSS Color Ramp ###
    # norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    # cax = fig.add_axes([0.91, 0.09, 0.02, 0.20])  # colorbar
    # cb = mpl.colorbar.ColorbarBase(
    #     cax, cmap=cmap, norm=norm, orientation="vertical", extend="both"
    # )
    # cb.outline.set_visible(False)
    # cb.set_label("Predicted Height in meters (NAVD88)", fontsize=13)
    # cb.set_ticks(np.arange(vmin, vmax + 1, np.abs((vmin - vmax) / 4)))

    # Write to image file
    im = serialize_to_buffer(fig, dpi=dpi)
    plt.close(fig)

    #    pic = serialize_to_pickle(fig)
    # Save as a pickle file
    #     pickle.dump(fig, base_fig_buf)
    #     plt.close(fig)

    return im