import cv2
import mediapipe as mp
from files.save_get_file import get_file_by_user


def image_params(*args):
    img = cv2.imread(get_file_by_user(1, 1))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    return img, img_rgb, height, width


def background():
    img = image_params()
    background_img = cv2.imread(get_file_by_user(1, 2))
    resized_bg_img = cv2.resize(background_img, (img[1].shape[1], img[0].shape[0]))
    return resized_bg_img


def mp_mesh():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.75)
    return mp_face_mesh, face_mesh


