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


variable "api_source_dir" {
  type = string
}

variable "app_name" {
  type = string
}

variable "app_short_name" {
  type = string
}


variable "vpc_id" {
  type        = string
  description = "The ID of the VPC to create the resources in"
}

variable "public_subnets" {
  type        = list(string)
  description = "The public subnets to deploy on"
}

variable "private_subnets" {
  type        = list(string)
  description = "The private subnets to deploy on"
}

variable "environment" {
  type = string
}

variable "cpu" {
  type    = number
  default = 1024
}

variable "memory" {
  type    = number
  default = 2048
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "db_host" {
  type = string
}

variable "db_port" {
  type    = string
  default = "5432"
}

variable "db_user" {
  type    = string
  default = "user"
}

variable "db_password" {
  type      = string
  default   = "password"
  sensitive = true
}

variable "env_arn_map" {
  type = map(string)
}

variable "api_fqdn" {
  type = string
}

variable "api_subdomain" {
  type = string
}

variable "acm_certificate_arn" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "sentry_organization_slug" {
  type = string
}

variable "enable_dev_endpoints" {
  type    = bool
  default = false
}