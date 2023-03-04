import cv2
import mediapipe as mp


def face_find():
    """ Параметры отрисовки маски """
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, min_detection_confidence=0.75)

    """ Картинка с которой работаем """
    img = cv2.imread(f'{config.ROOT_DIR}/test_img/{file_id}', 1)
    height, width, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    """ Накладывание точек на лицо """
    result = face_mesh.process(rgb_img)
    face = True
    if face:
        for facial_landmarks in result.multi_face_landmarks:
            for i in range(468):
                pt1 = facial_landmarks.landmark[i]
                x = int(pt1.x * width)
                y = int(pt1.y * height)
                cv2.circle(img, (x, y), 1, (250, 100, 255), -1)
                """ Соединение точек на лице"""
                mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=facial_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
    else:
        return f"Лицо не найдено"

    """ Результат """
    cv2.imshow("Res", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    face_find()
