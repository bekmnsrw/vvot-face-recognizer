import piexif

from PIL import Image
from io import BytesIO

def get_image(path):
    with Image.open(path) as image:
        image.load()
        
    return image

def save_image(image, path, exif=()):
    image.save(path, exif=piexif.dump(exif))

def get_image_bytes(path):
    with Image.open(path) as img:
        buffer = BytesIO()
        img.save(buffer, format=img.format)
        buffer.seek(0)
        return buffer