# Переменные

variable "api_gw_name" {
    type        = string
    description = "Название Yandex API Gateway"
    default     = "vvot09-apigw"
}

# Ресурсы

resource "yandex_api_gateway" "api_gw" {
    name = var.api_gw_name
    spec = <<-EOT
        openapi: "3.0.0"
        info:
            version: 1.0.0
            title: Face Recognizer API
        paths:
            /:
                get:
                    summary: Get images with faces by key
                    parameters:
                        - name: face
                            in: query
                            description: Key of the object with face image 
                            required: true
                            schema:
                                type: string
                    x-yc-apigateway-integration:
                        type: object_storage
                        object: "{face}"
                        bucket: ${yandex_storage_bucket.faces_bucket.bucket}
                        service_account_id: ${yandex_iam_service_account.sa_face_recognizer.id}
    EOT
}
