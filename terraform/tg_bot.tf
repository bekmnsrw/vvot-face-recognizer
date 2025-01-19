# Переменные

variable "tg_bot_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая обрабатывает сообщения, отправляемые Telegram боту"
    default     = "vvot09-tg-bot"
}

# Ресурсы

resource "yandex_function" "tg_bot_fun" {
    name               = var.tg_bot_fun_name
    entrypoint         = "index.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.tg_bot.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa_face_recognizer.id
    environment = {
        TG_BOT_KEY    = var.tg_bot_key
        PHOTOS_BUCKET = yandex_storage_bucket.photos_bucket.bucket
        FACES_BUCKET  = yandex_storage_bucket.faces_bucket.bucket
    }
    content {
        zip_filename = data.archive_file.tg_bot.output_path
    }
    mounts {
        name = yandex_storage_bucket.photos_bucket.bucket
        mode = "ro"
        object_storage {
            bucket = yandex_storage_bucket.photos_bucket.bucket
        }
    }
    mounts {
        name = yandex_storage_bucket.faces_bucket.bucket
        mode = "rw"
        object_storage {
            bucket = yandex_storage_bucket.faces_bucket.bucket
        }
    }
}

resource "yandex_function_iam_binding" "tg_bot_fun_iam_binding" {
    function_id = yandex_function.tg_bot_fun.id
    role        = "functions.functionInvoker"
    members     = [ "system:allUsers" ]
}

resource "telegram_bot_webhook" "tg_bot_webhook" {
    url = "https://functions.yandexcloud.net/${yandex_function.tg_bot_fun.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_face_recognizer_storage_editor_role" {
    folder_id = var.folder_id
    role      = "storage.editor"
    member    = "serviceAccount:${yandex_iam_service_account.sa_face_recognizer.id}"
}

# ZIP-архив

data "archive_file" "tg_bot" {
    type        = "zip"
    source_dir  = "../src/tg_bot"
    output_path = "../build/tg_bot.zip"
}
