from os import path, makedirs
from typing import Tuple, Union
from io import BytesIO
from datetime import datetime

from PIL import Image
from pymodm.files import ImageFieldFile

from imagefilefield.smartcrop import smart_crop


class ImageFieldToFile(ImageFieldFile):

    @property
    def images(self):
        sizes = self.get_sizes
        media_url = self.field.media_url
        images = {}

        for key in sizes.keys():
            media_path = path.join(
                media_url,
                "{}_{}.{}".format(key, str(self.file_id), self.image.format.lower()))
            media_path = ("{:%s}" % (media_path)).format(self.file.uploadDate)
            images[key] = media_path
        return images

    @property
    def get_sizes(self):
        return self.field.image_sizes or getattr(self.instance, "IMAGE_SIZES", None)

    def create_image_path(self, key: str) -> str:
        # file path
        fpath = path.join(
            self.field.upload_to,
            "{}_{}.{}".format(key, str(self.file_id), self.image.format.lower()))
        fpath = "{:%s}" % (fpath)
        fpath = fpath.format(datetime.utcnow())
        # try create folder path if not exists
        folder_path = "/".join(fpath.split("/")[:-1])
        try:
            makedirs(folder_path)
        except FileExistsError:
            pass

        return fpath

    def image_to_file(self, key: str, size: Tuple[int, int],
                      image_path: str=None, smartcrop: bool = False) -> str:
        '''
        method for convert image to desired size
        image: image binary file or image buffer
        size: (width, height)
        smart_crop: if not active will only use PIL `thumbnail` resizer
        '''
        fpath = self.create_image_path(key)
        # image data could be path file or BytesIo data
        image_data: Union[BytesIO, str]
        if image_path:
            image_data = image_path
        else:
            image_data = BytesIO()
            self.image.save(image_data, self.image.format)

        if smartcrop:
            smart_crop(image_data, size[0], size[1], fpath, True)
        else:
            img = Image.open(image_data)
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(fpath, self.image.format)

        return fpath

    def create_image_sizes(self) -> None:
        image_sizes = self.get_sizes
        if not image_sizes:
            return

        default = image_sizes.get("default")
        # default_image will be use for other image sizes
        default_image = None
        # create default image
        if default:
            default_image = self.image_to_file("default", default["size"],
                                               smartcrop=default.get("smartcrop"))

        # create other image sizes except default
        for key, params in image_sizes.items():
            if key == "default":
                continue

            self.image_to_file(key, params["size"], image_path=default_image,
                               smartcrop=params.get("smartcrop"))
