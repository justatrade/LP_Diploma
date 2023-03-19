from treatment import get_mask
from image import *
import cv2


def get_longest_contur(contours: tuple) -> int:
    longest = contours[0]
    for each in contours:
        if len(each) > len(longest):
            longest = each
    return longest


def draw_contours(img):
    img_rgb = image_params()[0]
    img = get_mask(img_rgb)
    contours, _ = cv2.findContours(image=img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    longest_contur = get_longest_contur(contours)
    cv2.drawContours(image=img_rgb, contours=longest_contur, contourIdx=-1, color=(0, 0, 255),
                     thickness=2,
                     lineType=cv2.LINE_AA)
    cv2.imshow("res", img_rgb)
    cv2.waitKey(0)


if __name__ == "__main__":
    draw_contours(image_params())
