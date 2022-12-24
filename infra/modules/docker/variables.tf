variable "source_dir" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "ecr_id" {
  type = string
}

variable "build_args" {
  type = map(string)
  default = {}
}