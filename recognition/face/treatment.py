import numpy as np
from numpy.typing import NDArray
from constant import *
from image import *


def image_zeros():
    img = image_params()
    dimension_chanel = (img[2], img[3], 1)
    image = np.zeros(dimension_chanel, dtype=np.uint8)
    image[:] = MASK_COLOR
    bg_image = np.zeros(dimension_chanel, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    return image, bg_image


def get_mask(img: NDArray) -> NDArray:
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)

    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = selfie_segmentation.process(image_rgb)

    condition = np.stack((result.segmentation_mask,), axis=-1) > 0.5

    output_image = np.where(condition, image_zeros()[0], image_zeros()[1])

    return output_image


