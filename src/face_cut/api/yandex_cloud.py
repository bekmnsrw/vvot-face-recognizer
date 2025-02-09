from PIL import Image
from pathlib import Path
from uuid import uuid4
from util.environment import FACES_BUCKET, PHOTOS_BUCKET
from util.constants import STORAGE_PREFIX

import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

"""
Docs: 
    - [Yandex Cloud. Object](https://yandex.cloud/ru/docs/storage/concepts/object)
"""

def get_original_photo(original_photo_id):
    photo_path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, original_photo_id)
    with Image.open(photo_path) as image:
        image.load()
    
    return image

def get_face_uid():
    face_uid = f"{uuid4()}.jpg"
    logger.debug(face_uid)
    
    return face_uid 

def upload_face(face, face_id):
    face_path = Path(STORAGE_PREFIX, FACES_BUCKET, face_id)
    face.save(face_path)
