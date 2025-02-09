import cv2

def get_faces_coordinates(image_path):
    image = cv2.imread(image_path)
    max_width, max_height = 1920, 1080
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

    original_height, original_width = image.shape[:2]

    if original_width > max_width or original_height > max_height:
        scaling_factor = min(max_width / original_width, max_height / original_height)
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        additional_scaling_factor = 0.90
        new_width = int(image.shape[1] * additional_scaling_factor)
        new_height = int(image.shape[0] * additional_scaling_factor)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    resized_height, resized_width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    original_faces = []
    
    for (x, y, w, h) in faces:
        x_original = int(x * (original_width / resized_width))
        y_original = int(y * (original_height / resized_height))
        w_original = int(w * (original_width / resized_width))
        h_original = int(h * (original_height / resized_height))
        original_faces.append([x_original, y_original, w_original, h_original])

    return original_faces