# from etss_animate import extend_extent
# from etss_animate import basemap_image

##### NOTE #####
# I want to be able to exactly equalize these extents, but it's currently
# just at a place that's "pretty good". It works well for most locations,
# but if the maps get very large, or if we get north of 70ish degrees, we
# start to see white space appear. This is (I think) because of the scale factor
# for the Mercator projection. I am taking the scale into account, but not
# exactly correctly, apparently.


# def test_extend_extent_aspect():
#     """Test that the updated extent matches the aspect ratio of
#     the output.
#     """

#     extent = (230, 260, 40, 76)

#     out_resolution = basemap_image.get_resolution("1080p")
#     fig_size = basemap_image.resolution_to_figsize(out_resolution)

#     fig_aspect = fig_size[0] / fig_size[1]

#     updated_extent = extend_extent.extend_extent(extent, fig_size)

#     updated_extent_width = updated_extent[1] - updated_extent[0]
#     updated_extent_height = updated_extent[3] - updated_extent[2]
#     updated_extent_aspect = updated_extent_width / updated_extent_height

#     assert updated_extent_aspect == fig_aspect
