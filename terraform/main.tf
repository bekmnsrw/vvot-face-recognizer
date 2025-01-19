# Переменные

variable "cloud_id" {
    type        = string
    description = "Идентификатор облака в Yandex Cloud"
}

variable "folder_id" {
    type        = string
    description = "Идентификатор каталога в Yandex Cloud"
}

variable "tg_bot_key" {
    type        = string
    description = "Токен Telegram бота"
}

variable "sa_name" {
    type        = string
    description = "Название сервисного аккаунта"
    default     = "sa-vvot09-face-recognizer"
}

variable "sa_key_file_path" {
    type        = string
    description = "Путь к авторизованному ключу сервисного аккаунта"
    default     = "~/.yc-keys/key.json"
}

variable "yandex_zone" {
    type        = string
    description = "Зона доступности Yandex Cloud"
    default     = "ru-central1-a"
}

# Обязательные провайдеры

terraform {
    required_providers {
        yandex = {
            source = "yandex-cloud/yandex"
        }
        telegram = {
            source  = "yi-jiayu/telegram"
            version = "0.3.1"
        }
    }
    required_version = ">= 0.13"
}

provider "yandex" {
    cloud_id                 = var.cloud_id
    folder_id                = var.folder_id
    zone                     = var.yandex_zone
    service_account_key_file = pathexpand(var.sa_key_file_path)
}

provider "telegram" {
    bot_token = var.tg_bot_key
}

# Общие ресурсы

resource "yandex_iam_service_account" "sa_face_recognizer" {
    name = var.sa_name
}
