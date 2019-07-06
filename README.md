# PyMODM-ImageFileField
ImageFileField for PyMODM

Configuration Media Path and Media Url
```
import imagefilefield

# Required
imagefilefield.FILEFIELD_MEDIA_PATH = os.path.join(BASE_DIR, "media/")
# Optional
imagefilefield.FILEFIELD_MEDIA_URL = "/media/" # Default Value

```


```
from os.path import join

from pymodm import MongoModel, fields
from imagefilefield.fields import ImageFileField

class TestImage(MongoModel):
    IMAGE_SIZES = {
        "small": {"size": (200, 200)},
        "medium": {"size": (625, 625)},
        "default": {"size": (800, 800), "smartcrop": True}
        # if key `default`, other sizes will based this size
        # `smartcrop` will use image detection on crop
    }

    text = fields.CharField()
    image = ImageFileField(
        upload_to=join(MEDIA_ROOT, "test_image/%Y/%m/%d/"), 
        blank=True)
    # using custom size
    image2 = ImageFileField(
        upload_to=join(MEDIA_ROOT, "test_image/%Y/%m/%d/"), 
        blank=True,
        image_sizes = {
          "small": {"size": (200, 100), "smartcrop": True},
          "medium": {"size": (525, 625), "smartcrop": True},
          "big": {"size": (700, 700), "smartcrop": True}
        })
    created = fields.DateTimeField(default=timezone.now)

```
