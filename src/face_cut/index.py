import ydb
import ydb.iam
from json import loads
from api.yandex_cloud import get_original_photo, upload_face, get_face_uid
from api.face_cutter import cut_face
from util.environment import YDB_ENDPOINT, YDB_PATH

"""
Docs:
    - [Yandex Cloud. Message Queue Trigger](https://yandex.cloud/ru/docs/functions/concepts/trigger/ymq-trigger)
"""

def handler(event, context):
    queue_message_body = event["messages"][0]["details"]["message"]["body"]
    message = loads(queue_message_body)

    original_photo_id, face_coordinates = message["original_photo_id"], message["face_coordinates"]
    original_photo = get_original_photo(original_photo_id)
    
    face = cut_face(original_photo, face_coordinates)
    face_id = get_face_uid()

    db_driver = ydb.Driver(
        endpoint=f"grpcs://{YDB_ENDPOINT}",
        database=YDB_PATH,
        credentials=ydb.iam.MetadataUrlCredentials(),
    )

    db_driver.wait(fail_fast=True, timeout=30)

    db_client = ydb.TableClient(db_driver)
    db_session = db_client.session().create()

    save_relation(db_session, original_photo_id, face_id)
    upload_face(face, face_id)

    return {
        "statusCode": 200,
    }

def save_relation(session, original_photo_id, face_id):
    query = f"INSERT INTO photos (photo_id, face_id, is_processing) VALUES ('{original_photo_id}', '{face_id}', FALSE)"
    session.transaction().execute(query, commit_tx=True)