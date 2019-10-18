from etss_animate import basemap_image
from PIL import ImageFile

# Is the output an image file?
def test_base():
    base = basemap_image.make_basemap(limit=2, extent=(170, 255, 40, 76))

    assert isinstance(base, ImageFile.ImageFile)


# Does it have the correct size given input?
def test_1080p():
    base = basemap_image.make_basemap(
        limit=2, extent=(170, 255, 40, 76), resolution="1080p"
    )

    assert base.size == (1920, 1080)


def test_720p():
    base = basemap_image.make_basemap(
        limit=2, extent=(170, 255, 40, 76), resolution="720p"
    )

    assert base.size == (1080, 720)
