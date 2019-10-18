from etss_animate import basemap_image
from PIL import ImageFile

def test_base():
    """Is the output an image file?"""
    base = basemap_image.make_basemap(limit=2, extent=(170, 255, 40, 76))

    assert isinstance(base, ImageFile.ImageFile)


def test_1080p_output_size():
    """Does the image have the correct ouput size if 1080p is selected?"""
    base = basemap_image.make_basemap(
        limit=2, extent=(170, 255, 40, 76), resolution="1080p"
    )

    assert base.size == (1920, 1080)


def test_720p_output_size():
    """Does the image have the correct ouput size if 720p is selected?"""

    base = basemap_image.make_basemap(
        limit=2, extent=(170, 255, 40, 76), resolution="720p"
    )

    assert base.size == (1080, 720)
