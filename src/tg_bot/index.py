from json import loads
from api.telegram import send_message, send_photo
from api.yandex_cloud import get_unrecognized_face, get_original_photos_with, get_face_by_id, update_metadata
from util.constants import GET_FACE, FIND
from util.constants import ERROR_MESSAGE, NO_UNRECOGNIZED_FACES_MESSAGE, NO_PHOTOS_WITH
from util.environment import API_GW_URL, FACES_BUCKET
from util.metadata import set_photo_uid, set_person_name

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

    # Пользователь отправил команду `/getface`
    if text == GET_FACE:
        unrecognized_face_key = get_unrecognized_face()

        if not unrecognized_face_key:
            send_message(NO_UNRECOGNIZED_FACES_MESSAGE, message)
            return
        
        photo_tg_uid = send_photo(f"{API_GW_URL}?face={unrecognized_face_key}", message)
        update_metadata(FACES_BUCKET, unrecognized_face_key, set_photo_uid, photo_tg_uid)
    
    # Пользователь в ответ на фото с лицом человека, полученное после команды `/getface`, отправил текст с именем этого человека
    elif text and (reply_message := message.get("reply_to_message")):
        photo_tg_uid = reply_message.get("photo")[-1].get("file_unique_id")

        if not photo_tg_uid:
            return
        
        face = get_face_by_id(photo_tg_uid)
        update_metadata(FACES_BUCKET, face, set_person_name, text)

    # Пользователь отправил команду `/find xyz`, где `xyz` - имя человека, фотографии с которым нужно найти
    elif text.startswith(FIND):
        name = text[(len(FIND) + 1):]
        original_photos_with = get_original_photos_with(name)

        if not original_photos_with:
            send_message(f"{NO_PHOTOS_WITH} {name}")
            return
    
        # TODO: Отправить все фотографии с `name` как альбом
    
    # Пользователь отправил неподдерживаемую ботом команду
    else:
        send_message(ERROR_MESSAGE, message)
