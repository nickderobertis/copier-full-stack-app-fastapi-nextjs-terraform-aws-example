variable "app_name" {
  type = string
}

variable "service_name" {
  type = string
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

