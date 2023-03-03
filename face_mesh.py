import cv2
import mediapipe as mp

# Face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mash = mp_face_mesh.FaceMesh()

# Image
img = cv2.imread(f'{config.ROOT_DIR}/test_img/{file_id}', 1)
height, width, _ = img.shape
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# Facial landmarks
result = face_mash.process(rgb_img)

for facial_landmarks in result.multi_face_landmarks:
    for i in range(0, 468):
        pt1 = facial_landmarks.landmark[i]
        x = int(pt1.x * width)
        y = int(pt1.y * height)
        cv2.circle(img, (x, y), 1, (100, 100, 0), -1)


cv2.imshow("Res", img)
cv2.waitKey(0)