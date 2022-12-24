variable "fe_subdomain" {
  type        = string
  description = "The sub-domain name of the frontend, e.g. for fe.staging.example.com it would be fe.staging"
}

variable "fe_fqdn" {
  type        = string
  description = "The fully qualified domain name of the frontend, e.g. staging.example.com"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "health_check_interval" {
  type    = number
  default = 30
  validation {
    condition     = contains([10, 30], var.health_check_interval)
    error_message = "Valid values for var: health_check_interval are (10, 30)."
  }
}

variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the records in"
}

variable "route53_zone_name" {
  type        = string
  description = "The name of the Route53 zone to create the records in"
}

variable "record_type" {
  type        = string
  description = "The type of the record to create"
  default     = "A"
  validation {
    condition     = contains(["A", "CNAME"], var.record_type)
    error_message = "Valid values for var: record_type are (A, CNAME)."
  }
}
