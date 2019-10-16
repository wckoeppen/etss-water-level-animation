#!/user/bin/env python
# coding=utf-8

import cartopy
import matplotlib.pyplot as plt
from cmocean import cm
import math
import matplotlib as mpl
import numpy as np
import io
from PIL import Image
import pickle


def serialize_to_image(in_figure_object):
    out_buffer = io.BytesIO()
    in_figure_object.savefig(out_buffer, bbox_inches="tight", format="PNG")
    out_image = Image.open(out_buffer)

    return out_image


# def serialize_to_pickle(in_figure_object):
#     out_buffer = io.BytesIO()
#     cloudpickle.dump(in_figure_object, out_buffer)

#     return out_buffer


def make_basemap(limit=0, extent=False):
    """
    Return a basemap image (PNG) with a coastline and rivers.
    
    Parameters
    ----------
    extent: (float, float, float, float), default:False
        Tuple of floats representing the required extent
        (x0, x1, y0, y1)

    limit: integer, default: 0
        The limits of the legend, which should match the
        gridded data
    
    Returns
    -------
    PNG
        A png image serialized by this function.
    """
    plate_crs = cartopy.crs.PlateCarree()
    merc_crs = cartopy.crs.Mercator(central_longitude=210)

    land_color = "#fcfcfc"
    coast_color = "#b1b1b1"
    # ocean_color = "#d7dfe0"
    # box_alpha = 0.7
    # annotation_spacing = 0.2
    cmap = cm.balance

    fig = plt.figure(dpi=72, figsize=(14, 14))
    ax = fig.add_axes([0, 0, 1, 1], projection=merc_crs)
    ax.outline_patch.set_visible(False)

    if not extent:
        extent = (170, 255, 40, 76)

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
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cax = fig.add_axes([0.91, 0.09, 0.02, 0.20])  # colorbar
    cb = mpl.colorbar.ColorbarBase(
        cax, cmap=cmap, norm=norm, orientation="vertical", extend="both"
    )
    cb.outline.set_visible(False)
    cb.set_label("Predicted Height in meters (NAVD88)", fontsize=13)
    cb.set_ticks(np.arange(vmin, vmax + 1, np.abs((vmin - vmax) / 4)))

    # Write to image file
    im = serialize_to_image(fig)

#    pic = serialize_to_pickle(fig)
    # Save as a pickle file
    #     pickle.dump(fig, base_fig_buf)
    #     plt.close(fig)

    return im