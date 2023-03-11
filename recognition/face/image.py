import cv2
import mediapipe as mp


def image():
    img = cv2.imread("recognition/face/fake1.jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    return img, img_rgb, height, width


def background():
    background_img = cv2.imread("recognition/face/kosm.png")
    resized_bg_img = cv2.resize(background_img, (image()[1].shape[1], image()[0].shape[0]))
    return resized_bg_img


def mp_mesh():
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.75)
    return mp_face_mesh, face_mesh


