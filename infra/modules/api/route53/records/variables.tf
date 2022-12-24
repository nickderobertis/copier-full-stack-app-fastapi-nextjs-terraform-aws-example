variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the records in"
}

variable "route53_zone_name" {
  type        = string
  description = "The name of the Route53 zone to create the records in"
}

variable "lb_dns_name" {
  type        = string
  description = "The DNS name of the load balancer"
}

variable "api_record_name" {
  type        = string
  description = "The name of the API record"
  default     = "api"
}
