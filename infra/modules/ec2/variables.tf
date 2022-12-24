variable "app_name" {
  type        = string
  description = "The name of the application"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "instance_type" {
  description = "The instance type to use"
  default     = "t2.micro"
}

variable "instance_root_block_device_volume_size" {
  description = "The size of the root block device volume of the EC2 instance in GiB"
  default     = 8
}

variable "output_directory" {
  description = "The name of the directory to download the SSH keys to"
  default     = "generated"
}

variable "instance_name" {
    description = "The name of the instance"
}

variable "security_group_ids" {
  description = "The security group IDs to attach to the instance"
  type        = list(string)
}

variable "startup_script" {
  description = "The startup script to run on the instance"
  type        = string
}

variable "vpc_id" {
    description = "The ID of the VPC to create the monitoring server in"
    type        = string
}

variable "subnet_id" {
  type        = string
  description = "ID of AWS subnet to put the instance in. Should be in the same VPC matching the passed vpc_id"
}

variable "iam_instance_profile" {
  type        = string
  description = "The IAM instance profile to attach to the instance"
  default = null
}