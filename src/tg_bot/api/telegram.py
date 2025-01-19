from requests import post
from util.environment import TG_API_URL

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
