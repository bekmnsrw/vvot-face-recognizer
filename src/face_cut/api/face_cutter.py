def cut_face(image, face_coordinates):
    left, upper, w, h = face_coordinates
    right = left + w + 1
    lower = upper + h + 1

    return image.crop((left, upper, right, lower))