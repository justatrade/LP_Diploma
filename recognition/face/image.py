import cv2
import mediapipe as mp
import pprint
import config


def image_params(img):
    """
    :param img: str
    :return: img - class 'numpy.ndarray', img_rgb - class 'numpy.ndarray', height - int, width - int
    """
    img = cv2.imread(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    if config.SPACE_DEBUG_MODE:
        pprint.pprint(img)
        pprint.pprint(img_rgb)
        pprint.pprint(height)
        pprint.pprint(width)
    return img, img_rgb, height, width


def mp_mesh():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.75)
    if config.SPACE_DEBUG_MODE:
        pprint.pprint(mp_face_mesh)
        pprint.pprint(face_mesh)
    return mp_face_mesh, face_mesh


