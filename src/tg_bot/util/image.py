import piexif

from PIL import Image

def get_image(path):
    with Image.open(path) as image:
        image.load()
        
    return image

def save_image(image, path, exif=()):
    image.save(path, exif=piexif.dump(exif))
