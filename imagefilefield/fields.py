from pymodm.fields import ImageField

from imagefilefield.files import ImageFieldToFile


class ImageFileField(ImageField):
    _wrapper_class = ImageFieldToFile

    def __init__(self, *args, **kwargs):
        # add custom params upload_to
        if not kwargs.get("upload_to"):
            raise ValueError("upload_to params is required")
        self.upload_to = kwargs.pop("upload_to")
        self.image_sizes = kwargs.pop("image_sizes", None)
        self.media_url = kwargs.pop("media_url", "/media/")
        super().__init__(*args, **kwargs)

    def to_mongo(self, value):
        file_obj = self.to_python(value)
        # Save the file and return its name.
        if not file_obj._committed:
            file_obj.save(value.file_id, value)

            # create image with specific sizes settings
            file_obj.create_image_sizes()

        return file_obj.file_id
