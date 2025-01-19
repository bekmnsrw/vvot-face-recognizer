from requests import post
from json import dumps
from util.environment import TG_API_URL
from util.image import get_image_bytes

def send_message(text, message):
    url = f"{TG_API_URL}/sendMessage"

    json = {
        "chat_id": message["chat"]["id"],
        "text": text,
        "reply_parameters": { 
            "message_id": message["message_id"],
        },
    }

    post(url=url, json=json)

def send_photo(path, message):
    url = f"{TG_API_URL}/sendMessage"
    
    json = {
        "chat_id": message["chat"]["id"],
        "photo": path,
        "reply_parameters": { 
            "message_id": message["message_id"],
        },
    }

    response = post(url=url, json=json)

    return response.json()["result"]["photo"][-1]["file_unique_id"]

def send_photos(paths, message):
    url = f"{TG_API_URL}/sendMediaGroup"

    for group in groups(paths, 10):
        media = [{"type": "photo", "media": f"attach://{path.name}"} for path in group]
        files = { path.name: get_image_bytes(path) for path in group }

        json = {
            "chat_id": message["chat"]["id"],
            "media": dumps(media),
            "reply_parameters": { 
                "message_id": message["message_id"],
            },
        }

        post(url=url, json=json, files=files)

def groups(paths, n):
    for i in range(0, len(paths), n):
        yield paths[i:(i + n)]