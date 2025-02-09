import base64
from pathlib import Path
from util.environment import PHOTOS_BUCKET, FACES_BUCKET
from util.constants import STORAGE_PREFIX

def handler(event, context):
    query_params = event.get('queryStringParameters', {})
    
    face_id = query_params.get('face')
    photo_id = query_params.get('original_photo')

    if not face_id and not photo_id:
        return {
            'statusCode': 400,
            'body': 'Missing query parameter: face or original_photo',
        }

    if face_id:
        path = Path(STORAGE_PREFIX, FACES_BUCKET, face_id)
    else:
        path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, photo_id)

    if not path.exists():
        return {
            'statusCode': 404,
            'body': f'File not found: {path}',
        }
    
    try:
        with open(path, "rb") as file:
            bytes = file.read()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error reading file: {e}',
        }

    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'image/jpeg' },
        'body': base64.b64encode(bytes).decode("utf-8"),
        'isBase64Encoded': True,
    }