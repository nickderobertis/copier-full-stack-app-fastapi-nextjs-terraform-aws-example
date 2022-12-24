variable "app_name" {
  type        = string
  description = "The name of the application"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}
