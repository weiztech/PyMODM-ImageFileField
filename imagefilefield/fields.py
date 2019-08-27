from pymodm.fields import ImageField
from bson import ObjectId

from imagefilefield.files import ImageFieldToFile
import imagefilefield


class ImageFileField(ImageField):
    _wrapper_class = ImageFieldToFile

    @property
    def base_media_path(self):
        return imagefilefield.FILEFIELD_MEDIA_PATH

    @property
    def base_media_url(self):
        return imagefilefield.FILEFIELD_MEDIA_URL

    def __init__(self, *args, **kwargs):
        # add custom params upload_to
        if not kwargs.get("upload_to"):
            raise ValueError("upload_to params is required")
        self.upload_to = kwargs.pop("upload_to")
        self.image_sizes = kwargs.pop("image_sizes", None)
        super().__init__(*args, **kwargs)

    def to_mongo(self, value):
        file_obj = self.to_python(value)

        if isinstance(file_obj, ObjectId):
            return file_obj

        # Save the file and return its name.
        if not file_obj._committed:
            if not self.base_media_path:
                raise ValueError(
                    "imagefilefield.FILEFIELD_MEDIA_PATH cannot be none")

            file_obj.save(value.file_id, value)

            # load saved gridfs files data from storage
            # for make the data available to next process
            file_obj.file = file_obj.storage.open(file_obj.file_id)

            # create image with specific sizes settings
            file_obj.create_image_sizes()

        return file_obj.file_id
