from PIL import Image

def cut_face(image, face_coordinates, min_size=320):
    left, upper, w, h = face_coordinates
    right = left + w
    lower = upper + h

    cropped_image = image.crop((left, upper, right, lower))

    if cropped_image.width < min_size or cropped_image.height < min_size:
        scale_factor = max(min_size / cropped_image.width, min_size / cropped_image.height)
        new_width = int(cropped_image.width * scale_factor)
        new_height = int(cropped_image.height * scale_factor)

        cropped_image = cropped_image.resize((new_width, new_height), Image.LANCZOS)

    return cropped_image