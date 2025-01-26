from pathlib import Path
from api.yandex_cloud import send_message_to_queue
from api.face_detector import get_faces_coordinates
from util.environment import PHOTOS_BUCKET, STORAGE_PREFIX

"""
Docs: 
    - [Yandex Cloud. Cloud Functions / Object Storage Trigger](https://yandex.cloud/ru/docs/functions/concepts/trigger/os-trigger)
    - [Yandex Cloud. Message Queue](https://yandex.cloud/en/docs/message-queue/quickstart)
"""

def handler(event, context):
    image_id = event["messages"][0]["details"]["object_id"]

    image_path = Path(STORAGE_PREFIX, PHOTOS_BUCKET, image_id)
    faces = get_faces_coordinates(image_path)

    for face in faces:
        queue_message_body = {
            "image_id": image_id,
            "face_coordinates": face,
        }

        send_message_to_queue(queue_message_body)

    return {
        "statusCode": 200,
    }