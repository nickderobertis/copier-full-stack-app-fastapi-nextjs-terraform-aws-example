variable "app_name" {
    type        = string
    description = "The name of the application"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "sns_topic_arn" {
  type        = string
  description = "The ARN of the SNS topic to send alerts to"
}

variable "aws_region" {
  type        = string
  description = "The AWS region to deploy to"
}