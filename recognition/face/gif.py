from files.save_get_file import get_file_by_user
from recognition.face.image import image_params
from recognition.face.circuit import draw_contours
from PIL import Image
import glob
import os


def gif(img):
    frames = []
    imgs = glob.glob("image_gif/*.jpg")
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    frames[0].save("jpg_to_gif.gif", format="GIF", append_images=frames[::1],
                   save_all=True, duration=300, loop=0)

    n = 0
    for i in range(len(imgs)):
        n += 1
        os.remove(f"image_gif/Контур_{n}.jpg")


if __name__ == "__main__":
    gif(draw_contours(image_params(get_file_by_user(1, 1))))
