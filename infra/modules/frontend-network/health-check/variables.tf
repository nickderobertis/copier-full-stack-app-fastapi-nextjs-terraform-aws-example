variable "tags" {
  type = map(string)
}

variable "web_fqdn" {
  type = string
}

variable "health_check_interval" {
  type = number
  validation {
    condition     = contains([10, 30], var.health_check_interval)
    error_message = "Valid values for var: health_check_interval are (10, 30)."
  }
}
