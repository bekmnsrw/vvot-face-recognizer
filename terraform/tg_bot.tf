# Переменные

variable "tg_bot_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая обрабатывает сообщения, отправляемые Telegram боту"
    default     = "vvot09-tg-bot"
}

# Ресурсы

resource "yandex_function" "tg_bot_fun" {
    name               = var.tg_bot_fun_name
    entrypoint         = "tg_bot.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.tg_bot.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa_vvot09_task2.id
    content {
        zip_filename = data.archive_file.tg_bot.output_path
    }
    environment = {
        TG_BOT_KEY = var.tg_bot_key
    }
}

resource "telegram_bot_webhook" "tg_bot_webhook" {
    url = "https://functions.yandexcloud.net/${yandex_function.tg_bot_fun.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_vvot09_task2_function_invoker_role" {
    folder_id = var.folder_id
    role      = "functions.functionInvoker"
    member    = "serviceAccount:${yandex_iam_service_account.sa_vvot09_task2.id}"
}

# ZIP-архив

data "archive_file" "tg_bot" {
    type        = "zip"
    source_dir  = "../src/tg_bot"
    output_path = "../build/tg_bot.zip"
}
