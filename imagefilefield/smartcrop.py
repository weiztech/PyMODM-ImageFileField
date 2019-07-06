import cv2
from numpy import asarray, uint8

from smartcrop import auto_center, auto_resize, exact_crop


def smart_crop(image, target_width, target_height, destination, do_resize):
    # read grayscale image
    try:
        original = cv2.imread(image)
    except TypeError:
        image.seek(0)
        file_binary = asarray(bytearray(image.read()), dtype=uint8)
        original = cv2.imdecode(file_binary, cv2.IMREAD_COLOR)

    if original is None:
        print("Could not read source image")
        return

    target_height = int(target_height)
    target_width = int(target_width)

    if do_resize:
        original = auto_resize(original, target_width, target_height)

    # build the grayscale image we will work onto
    matrix = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    height, width, depth = original.shape

    if target_height > height:
        print('Warning: target higher than image')

    if target_width > width:
        print('Warning: target wider than image')

    center = auto_center(matrix)

    crop_pos = exact_crop(center, width, height, target_width, target_height)

    cropped = original[
        int(crop_pos['top']): int(crop_pos['bottom']),
        int(crop_pos['left']): int(crop_pos['right'])]
    cv2.imwrite(destination, cropped)
