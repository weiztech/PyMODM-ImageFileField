from os import path, makedirs
from typing import Tuple, Union
from io import BytesIO

from PIL import Image
from pymodm.files import ImageFieldFile

from imagefilefield.smartcrop import smart_crop


class ImageFieldToFile(ImageFieldFile):

    def generate_image_path(self, key_size, base_path):
        '''
        return full image path
        '''
        media_path = path.join(
            base_path,
            self.field.upload_to,
            "{}_{}.{}".format(key_size, str(self.file_id), self.image.format.lower()))
        media_path = ("{:%s}" % (media_path)).format(self.file.uploadDate)
        return media_path

    @property
    def images(self):
        '''
        return url created images base on defined sizes
        '''
        sizes = self.get_sizes
        images = {}

        for key in sizes.keys():
            images[key] = self.generate_image_path(key, self.field.base_media_url)
        return images

    @property
    def get_sizes(self):
        '''
        return the specified image sizes
        '''
        return self.field.image_sizes or getattr(self.instance, "IMAGE_SIZES", None)

    def create_image_path(self, key: str) -> str:
        # file path
        fpath = self.generate_image_path(key, self.field.base_media_path)
        # try create folder path if not exists
        folder_path = "/".join(fpath.split("/")[:-1])
        try:
            makedirs(folder_path)
        except FileExistsError:
            pass

        return fpath

    def image_to_file(self, key: str, size: Tuple[int, int],
                      image_path: Union[BytesIO, str, None]=None,
                      smartcrop: bool = False) -> str:
        '''
        method for convert image to desired size
        image: image binary file or image buffer
        size: (width, height)
        smart_crop: if not active will only use PIL `thumbnail` resizer
        '''
        fpath = self.create_image_path(key)

        # image data could be path file or BytesIo data
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
