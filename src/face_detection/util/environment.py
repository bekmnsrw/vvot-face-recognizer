from os import getenv

PHOTOS_BUCKET = getenv("PHOTOS_BUCKET")
MESSAGE_QUEUE_URL = getenv("MESSAGE_QUEUE_URL")
ACCESS_KEY = getenv("ACCESS_KEY")
SECRET_KEY = getenv("SECRET_KEY")

STORAGE_PREFIX = "/function/storage"

# Настройки boto3 клиента

SERVICE_NAME = "sqs"
ENDPOINT_URL = "https://message-queue.api.cloud.yandex.net"
REGION_NAME = "ru-central1"