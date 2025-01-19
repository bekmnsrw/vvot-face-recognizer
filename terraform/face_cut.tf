# Переменные

variable "face_cut_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая создает фотографию лица"
    default     = "vvot09-face-cut"
}

variable "faces_bucket_name" {
    type        = string
    description = "Название бакета с изображениями лиц"
    default     = "vvot09-faces"
}

variable "face_cut_trigger_name" {
    type        = string
    description = "Название триггера для запуска обработчика `face-cut`"
    default     = "vvot09-task"
}

# Ресурсы

resource "yandex_function" "face_cut_fun" {
    name               = var.face_cut_fun_name
    entrypoint         = "face_cut.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.face_cut.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa_face_recognizer.id
    content {
        zip_filename = data.archive_file.face_cut.output_path
    }
}

resource "yandex_storage_bucket" "faces_bucket" {
    bucket = var.faces_bucket_name
}

resource "yandex_function_trigger" "face_cut_trigger" {
    name = var.face_cut_trigger_name
    message_queue {
        queue_id           = yandex_message_queue.tasks_queue.arn
        service_account_id = yandex_iam_service_account.sa_face_recognizer.id
        batch_cutoff       = 1 # Дефолтное значение в соответствии с документацией
        batch_size         = 1 # Дефолтное значение в соответствии с документацией
    }
    function {
        id                 = yandex_function.face_cut_fun.id
        service_account_id = yandex_iam_service_account.sa_face_recognizer.id
    }
}

# ZIP-архив

data "archive_file" "face_cut" {
    type        = "zip"
    source_dir  = "../src/face_cut"
    output_path = "../build/face_cut.zip"
}