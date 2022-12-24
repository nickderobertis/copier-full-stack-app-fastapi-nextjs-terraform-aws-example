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

variable "fe_subdomain" {
  type        = string
  description = "The sub-domain name of the frontend, e.g. for fe.staging.example.com it would be fe.staging"
}
