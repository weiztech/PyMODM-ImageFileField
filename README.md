# PyMODM-ImageFileField
ImageFileField for PyMODM

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
        blank=True, 
        media_url=join(MEDIA_URL, "test_image/%Y/%m/%d/"))
    # using custom size
    image2 = ImageFileField(
        upload_to=join(MEDIA_ROOT, "test_image/%Y/%m/%d/"), 
        blank=True,
        image_sizes = {
          "small": {"size": (200, 100), "smartcrop": True},
          "medium": {"size": (525, 625), "smartcrop": True},
          "big": {"size": (700, 700), "smartcrop": True}
        }
        media_url=join(MEDIA_URL, "test_image/%Y/%m/%d/"))
    created = fields.DateTimeField(default=timezone.now)

```
