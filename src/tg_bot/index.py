import ydb
import ydb.iam
from json import loads
from api.telegram import send_message, send_photo
from util.constants import GET_FACE, FIND
from util.constants import ERROR_MESSAGE, NO_UNRECOGNIZED_FACES_MESSAGE, NO_PHOTOS_WITH
from util.environment import API_GW_URL, YDB_ENDPOINT, YDB_PATH
from api.ydb import get_unrecognized_face_id, get_all_original_photos_with, save_name, get_processing_face_id, set_is_processing

"""
Docs:
    - [Yandex Cloud. Connecting to YDB from Cloud Function](https://yandex.cloud/ru/docs/ydb/tutorials/connect-from-cf)
"""

def handler(event, context):
    update = loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message)
    
    return {
        "statusCode": 200,
    }

def handle_message(message):
    text = message.get("text")

    db_driver = ydb.Driver(
        endpoint=f"grpcs://{YDB_ENDPOINT}",
        database=YDB_PATH,
        credentials=ydb.iam.MetadataUrlCredentials(),
    )

    db_driver.wait(fail_fast=True, timeout=30)

    db_client = ydb.TableClient(db_driver)
    db_session = db_client.session().create()

    # Пользователь отправил команду `/getface`
    if text == GET_FACE:
        try:
            unrecognized_face_id = get_unrecognized_face_id(db_session)
            set_is_processing(db_session, unrecognized_face_id, True)
            send_photo(f"{API_GW_URL}?face={unrecognized_face_id}", message)
        except Exception as e:
            send_message(NO_UNRECOGNIZED_FACES_MESSAGE, message)
        
        return {
            "statusCode": 200
        }
    
    # Пользователь в ответ на фото с лицом человека, полученное после команды `/getface`, отправил текст с именем этого человека
    elif text and (not text.startswith("/")):
        try:
            face_id = get_processing_face_id(db_session)
            save_name(db_session, text, face_id)
            set_is_processing(db_session, face_id, False)
        except Exception as e:
            send_message("qwerty", message)

        return {
            "statusCode": 200
        }

    # Пользователь отправил команду `/find xyz`, где `xyz` - имя человека, фотографии с которым нужно найти
    elif text.startswith(FIND):
        try:
            name = text[(len(FIND) + 1):]
            original_photos_with = get_all_original_photos_with(db_session, name)

            if original_photos_with:
                for original in original_photos_with:
                    send_photo(f"{API_GW_URL}?original_photo={original}", message)
            else:
                send_message(NO_PHOTOS_WITH.format(name), message)
        except Exception as e:
            send_message(ERROR_MESSAGE, message)
        
        return {
            "statusCode": 200
        }
    
    # Пользователь отправил неподдерживаемую ботом команду
    else:
        send_message(ERROR_MESSAGE, message)
        
        return {
            "statusCode": 200
        }
