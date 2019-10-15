# Steps to success
Historically I've tried to:
- pass a matplotlib figure object directly across worker boundaries (terrible results, because matplotlib is not threadsafe)
- pickle a matplotlib figure object and unpickle it on workers (still unsafe, because matplotlib and pickle; but got slightly better results but with unreliable and inconsistent errors)

For this work, I'm going to experiment I'm going to experiment with layers. I.e., build a basemap image, build data images, and add all the layers together as images with transparency. The images should be very safe, though I'm not quite sure what tools python has for combining multiple images like this.

## Build a base map image
Uses matplotlib and cartopy, and it will need the map bounds, projection, dpi of the desired output.

## Given an input deployment, calculate an output image size and bounds.
One method is to force every video to be some consistent size that is youtube ready. E.g., 1080p (1920 x 1080px) or 720p (1080 x 720 pixels, or square). In this case, when we just have max lat and lon of location data, we'll have to find the output lat and lon such that everything fits both the data and into our preferred output pixel size.

Another method would be to allow the videos to have free-form sizes (e.g., some could be tall, others wide, etc.). This is fine for most movie players, but not great for youtube.

## Add gridded data image
In this case, ETSS data, and perhaps wind direction arrows.


## Add vector data image
Bars representing the water levels.