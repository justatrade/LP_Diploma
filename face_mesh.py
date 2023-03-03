import cv2
import mediapipe as mp


def face_find():
    # Face mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.75)

    # Image
    img = cv2.imread(f'{config.ROOT_DIR}/test_img/{file_id}', 1)

    height, width, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Facial landmarks
    result = face_mesh.process(rgb_img)
    for facial_landmarks in result.multi_face_landmarks:
        for i in range(0, 468):
            pt1 = facial_landmarks.landmark[i]
            x = int(pt1.x * width)
            y = int(pt1.y * height)
            cv2.circle(img, (x, y), 1, (250, 100, 255), -1)
            # Here start compound landmarks
            mp_drawing.draw_landmarks(
                image=img,
                landmark_list=facial_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles
                .get_default_face_mesh_tesselation_style())
    # Result
    cv2.imshow("Res", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    face_find()
