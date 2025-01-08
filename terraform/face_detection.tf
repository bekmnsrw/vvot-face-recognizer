# Переменные

variable "face_detection_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая обнаруживает лица на оригинальной фотографии"
    default     = "vvot09-face-detection"
}

variable "photos_bucket_name" {
    type        = string
    description = "Название бакета с оригинальными фотографиями"
    default     = "vvot09-photos"
}

variable "tasks_queue_name" {
    type        = string
    description = "Название очереди сообщений с заданиями на создание фотографии лица"
    default     = "vvot09-tasks"
}

variable "upload_photo_trigger_name" {
    type        = string
    description = "Название триггера для запуска обработчика `face-detection`"
    default     = "vvot09-photo"
}

# Ресурсы

resource "yandex_function" "face_detection_fun" {
    name               = var.face_detection_fun_name
    entrypoint         = "face_detection.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.face_detection.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa_vvot09_task2.id
    content {
        zip_filename = data.archive_file.face_detection.output_path
    }
}

resource "yandex_storage_bucket" "photos_bucket" {
    name = var.photos_bucket_name
}

resource "yandex_message_queue" "tasks_queue" {
    name = var.tasks_queue_name
}

resource "yandex_function_trigger" "upload_photo_trigger" {
    name        = var.upload_photo_trigger_name
    description = "Триггер в ответ на загрузку оригинальной фотографии в бакет `photos_bucket`"
    object_storage {
        bucket_id = yandex_storage_bucket.photos_bucket.id
        suffix    = ".jpg"
        create    = true
    }
    function {
        id                 = yandex_function.face_detection_fun.id
        service_account_id = yandex_iam_service_account.sa_vvot09_task2.id
    }
}

resource "yandex_resourcemanager_folder_iam_member" "sa_vvot09_task2_storage_viewer_role" {
    folder_id = var.folder_id
    role      = "storage.viewer"
    member    = "serviceAccount:${yandex_iam_service_account.sa_vvot09_task2.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_vvot09_task2_ymq_writer_role" {
    folder_id = var.folder_id
    role      = "ymq.writer"
    member    = "serviceAccount:${yandex_iam_service_account.sa_vvot09_task2.id}"
}

# ZIP-архив

data "archive_file" "face_detection" {
    type        = "zip"
    source_dir  = "../src/face_detection"
    output_path = "../build/face_detection.zip"
}
