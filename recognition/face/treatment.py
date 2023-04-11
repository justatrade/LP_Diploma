import numpy as np
from numpy.typing import NDArray
from constant import MASK_COLOR, BG_COLOR
from recognition.face.image import *


def image_zeros(img: NDArray) -> NDArray:
    """

    :param img: NDArray
    :return: NDArray
    """
    height = img[2]
    width = img[3]
    dimension_chanel = (height, width, 1)
    image = np.zeros(dimension_chanel, dtype=np.uint8)
    image[:] = MASK_COLOR
    bg_image = np.zeros(dimension_chanel, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    if config.SPACE_DEBUG_MODE:
        pprint.pprint(image)
        pprint.pprint(bg_image)
    return image, bg_image


def get_mask(img: NDArray) -> NDArray:
    """

    :param img: NDArray
    :return: NDArray
    """
    shape = image_zeros(img)
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)
    image_rgb = cv2.cvtColor(img[0], cv2.COLOR_BGR2RGB)
    result = selfie_segmentation.process(image_rgb)
    condition = np.stack((result.segmentation_mask,), axis=-1) > 0.5
    output_image = np.where(condition, shape[0], shape[1])
    if config.SPACE_DEBUG_MODE:
        pprint.pprint(output_image)
    return output_image
