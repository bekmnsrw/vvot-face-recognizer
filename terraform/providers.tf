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
