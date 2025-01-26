from json import loads

"""
Docs:
    - [Yandex Cloud. Message Queue Trigger](https://yandex.cloud/ru/docs/functions/concepts/trigger/ymq-trigger)
"""

def handler(event, context):
    queue_message_body = event["messages"][0]["details"]["message"]["body"]
    message = loads(queue_message_body)

    image_id, face_coordinates = message["image_id"], message["face_coordinates"]

    # TODO: Cut each face

    return {
        "statusCode": 200,
    }