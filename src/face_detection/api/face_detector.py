import cv2

def get_faces_coordinates(image_path):
    image = cv2.imread(image_path)
    
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_image = clahe.apply(gray_image)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_classifier.detectMultiScale(
        image=gray_image,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )

    return list(map(__map_face_cooridanates, faces))

def __map_face_cooridanates(face):
    return [int(face[0]), int(face[1]), int(face[2]), int(face[3])]