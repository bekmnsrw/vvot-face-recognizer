from pathlib import Path
from PIL import Image
from util.environment import FACES_BUCKET
from util.image import get_image, save_image
from util.metadata import get_person_name, get_original_image_path, get_photo_uid

prefix = "/function/storage"

def get_unrecognized_face():
    for path in Path(prefix, FACES_BUCKET).iterdir():
        with Image.open(path) as image:
            image.load()
        
        if not get_person_name(image):
            return path.name

def get_original_photos_with(name):
    original_photos_with = []

    for path in Path(prefix, FACES_BUCKET).iterdir():
        with Image.open(path) as image:
            image.load()

        if get_person_name(image) == name:
            path = get_original_image_path(image)
            original_photos_with.append(path)
    
    return original_photos_with

def get_face_by_id(photo_uid):
    for path in Path(prefix, FACES_BUCKET).iterdir():
        with Image.open(path) as image:
            image.load()

        if get_photo_uid(image) == photo_uid:
            return path.name

def update_metadata(bucket, key, function, value):
    path = Path(prefix, bucket, key)
    image = get_image(path)
    metadata = function(image, value)
    save_image(image, path, metadata)
