from files.save_get_file import get_file_by_user
from numpy.typing import NDArray
from treatment import get_mask
from image import *


def get_longest_contur(contours: tuple) -> int:
    """

    :param contours: tuple
    :return: int
    """
    longest = contours[0]
    for each in contours:
        if len(each) > len(longest):
            longest = each
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
    cv2.drawContours(image=img_rgb[0], contours=longest_contur, contourIdx=-1, color=(0, 0, 255),
                     thickness=2,
                     lineType=cv2.LINE_AA)
    return longest_contur


if __name__ == "__main__":
    draw_contours(image_params(get_file_by_user(1, 1)))
