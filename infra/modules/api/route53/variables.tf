variable "lb_dns_name" {
  type        = string
  description = "The DNS name of the load balancer"
}

variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the records in"
}

variable "route53_zone_name" {
  type        = string
  description = "The name of the Route53 zone to create the records in"
}

variable "health_check_interval" {
  type    = number
  default = 30
  validation {
    condition     = contains([10, 30], var.health_check_interval)
    error_message = "Valid values for var: health_check_interval are (10, 30)."
  }
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "api_fqdn" {
  type = string
}

variable "api_subdomain" {
  type = string
}
