variable "app_name" {
  type        = string
  description = "The name of the app"
}

variable "db_subnet_group" {
  type        = string
  description = "The DB subnet group"
}

variable "vpc_id" {
  type        = string
  description = "The VPC ID"
}

variable "vpc_cidr_block" {
  type        = string
  description = "The VPC CIDR block"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}
