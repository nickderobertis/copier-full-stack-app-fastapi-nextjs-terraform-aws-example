variable "app_name" {
  type = string
}

variable "app_short_name" {
  type = string
}

variable "tags" {
  type = map(string)
}


variable "vpc_id" {
  type        = string
  description = "The VPC ID to deploy on"
}

variable "public_subnets" {
  type        = list(string)
  description = "The public subnets to deploy on"
}

variable "security_group_id" {
  type        = string
  description = "The security group to use for the load balancer"
}

variable "acm_certificate_arn" {
  type        = string
  description = "The ARN of the ACM certificate to use for the load balancer SSL"
}
