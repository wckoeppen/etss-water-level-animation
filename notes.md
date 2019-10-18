# Steps to success
Historically I've tried to:
- pass a matplotlib figure object directly across worker boundaries (terrible results, because matplotlib is not threadsafe)
- pickle a matplotlib figure object and unpickle it on workers (still unsafe, because matplotlib and pickle; but got slightly better results but with unreliable and inconsistent errors)

For this work, I'm going to experiment I'm going to experiment with layers. I.e., build a basemap image, build data images, and add all the layers together as images with transparency. The images should be very safe, though I'm not quite sure what tools python has for combining multiple images like this.

## Build a base map image
Uses matplotlib and cartopy, and it will need the map bounds, projection, dpi of the desired output.

There is a complicated relationship between the given extent (map bounds) and the pixel size of the output. For example, you might want to provide square-ish map bounds but still have a figure that fits into a video. In this case, we have to do some math to determine what the approximate map bounds should be to fill up the space expected.

## Given an input deployment, calculate an output image size and bounds.
One method is to force every video to be some consistent size that is youtube ready. E.g., 1080p (1920 x 1080px) or 720p (1080 x 720 pixels, or square). In this case, when we just have max lat and lon of location data, we'll have to find the output lat and lon such that everything fits both the data and into our preferred output pixel size.

Another method would be to allow the videos to have free-form sizes (e.g., some could be tall, others wide, etc.). This is fine for most movie players, but not great for youtube.

## Add gridded data image
In this case, ETSS data, and perhaps wind direction arrows.


## Add vector data image
Bars representing the water levels.

# Tests

## test_extend_extents.py
My goal was to be able to set one side of the map, and have the other side extend itself to fill up the output aspect ratio. This would be trivial if we were using a simple cyclindrical (plate carree) projection; however, it turns out that this was difficult (for me at least) because I'm using the Mercator projection. Mercator has a scale factor that's dependent on the latitude. Currently I'm using the center latitude to estimate the scale factor, and applying that in a haphazard way to the aspect ratios. It works pretty well, except when (a) the map is zoomed out (i.e., the center latitude is far away from the edges of the map) or (b) we're at high latitudes (e.g., >75). A future improvement would be to figure this out, but so far I'm not sure how. It might take an empirical approach, generating a lot of cartopy maps and calculating their aspect ratio directly. But the final extents must be kept around, because they'll need to be passed to each subsequent layer call.