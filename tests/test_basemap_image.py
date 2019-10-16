from etss_animate import basemap_image
from PIL import ImageFile

# Is the output an image file?
def test_base():
    base = basemap_image.make_basemap(limit=2, extent=(170, 255, 40, 76))
    assert isinstance(base, ImageFile.ImageFile)

#Does it have the correct size given input?
