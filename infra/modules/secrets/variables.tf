variable "app_name" {
  type        = string
  description = "The name of the application"
}

variable "service_name" {
  type        = string
  description = "The name of the service"
  default = "app"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "secrets" {
  type        = map(string)
  description = "The secrets to set for the application"
  default     = {}
}

variable "params" {
  type        = map(string)
  description = "The parameters to set for the application (non-secret environment variables)"
  default     = {}
}
