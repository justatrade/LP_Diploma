import cv2
import mediapipe as mp
import os
from w import *


def mesh(face=True):
    img = image()
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    result = mp_mesh()[1].process(img[1])
    if face:
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(468):
                pt1 = facial_landmarks.landmark[i]
                x = int(pt1.x * img[3])
                y = int(pt1.y * img[2])
                cv2.circle(img[0], (x, y), 1, (250, 100, 255), -1)
                mp_drawing.draw_landmarks(
                    image=img[0],
                    landmark_list=facial_landmarks,
                    connections=mp_mesh()[0].FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
        cv2.imshow("Res", img[0])
        cv2.waitKey(0)


mesh()
