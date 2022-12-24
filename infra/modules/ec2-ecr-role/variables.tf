variable "app_name" {
  type = string
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "ecr_arns" {
  type        = list(string)
  description = "The ARNs of the ECR repositories"
}

variable "extra_global_permissions" {
  type        = list(string)
  description = "Extra permissions to add to the global policy"
  default     = []
}