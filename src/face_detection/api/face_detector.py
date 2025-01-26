import cv2

"""
Docs:
    - [Face Detection with OpenCV](https://www.datacamp.com/tutorial/face-detection-python-opencv)
"""

def get_faces_coordinates(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    faces = face_classifier.detectMultiScale(
        image=gray_image, 
        scaleFactor=1.1, 
        minNeighbors=5,
    )

    return list(map(__map_face_cooridanates, faces))

def __map_face_cooridanates(face):
    return [int(face[0]), int(face[1]), int(face[2]), int(face[3])]