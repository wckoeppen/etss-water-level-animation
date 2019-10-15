#!/user/bin/env python
# coding=utf-8

import cartopy
import matplotlib


def make_basemap(limit=None, extent=False):
    """Create a basemap image.
    
    Keyword Arguments:
        limit {[type]} -- [description] (default: {None})
        extent {bool} -- [description] (default: {False})
    
    Returns:
        [type] -- [description]
    """

    plate_crs = cartopy.crs.PlateCarree()
    merc_crs = cartopy.crs.Mercator(central_longitude=210)

    land_color = "#fcfcfc"
    coast_color = "#b1b1b1"
    ocean_color = "#d7dfe0"
    box_alpha = 0.7
    annotation_spacing = 0.2
    cmap = cmocean.cm.balance

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
    if not limit:
        limit = math.ceil(np.max(np.abs(surge_image)))

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

    pic = serialize_to_pickle(fig)
    # Save as a pickle file
    #     pickle.dump(fig, base_fig_buf)
    #     plt.close(fig)

    return (im, pic)
