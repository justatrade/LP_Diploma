from numpy.typing import NDArray
from treatment import get_mask
from recognition.face.image import *


def get_longest_contur(contours: tuple) -> int:
    """

    :param contours: tuple
    :return: int
    """
    longest = contours[0]
    for each in contours:
        if len(each) > len(longest):
            longest = each
    if config.SPACE_DEBUG_MODE:
        pprint.pprint(longest)
    return longest


def draw_contours(img: tuple) -> NDArray:
    """

    :param img: class 'tuple'
    :return: class 'numpy.ndarray'
    """
    img_rgb = img
    img = get_mask(img_rgb)
    contours, _ = cv2.findContours(image=img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    longest_contur = get_longest_contur(contours)
    n = 0
    for i in range(len(longest_contur[::100])):
        n += 1
        cv2.drawContours(image=img_rgb[0], contours=longest_contur[:n*100:], contourIdx=-1, color=(0, 0, 255),
                         thickness=2,
                         lineType=cv2.LINE_AA)
        gif_frame = cv2.imwrite(f"image_gif/Контур_{n}.jpg", img_rgb[0])

    if config.SPACE_DEBUG_MODE:
        pprint.pprint(gif_frame)
        pprint.pprint(longest_contur)
    return gif_frame, longest_contur

