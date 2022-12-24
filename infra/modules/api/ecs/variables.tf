variable "app_name" {
  type = string
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

variable "vpc_id" {
  type = string
}

variable "lb_sg_id" {
  type = string
}

variable "private_subnets" {
  type = list(string)
}

variable "target_group_arn" {
  type = string
}

variable "docker_image_name" {
  type = string
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


variable "tags" {
  type = map(string)
}

variable "aws_region" {
  type = string
}

variable "sentry_dsn" {
  type = string
}

variable "enable_dev_endpoints" {
  type    = bool
  default = false
}