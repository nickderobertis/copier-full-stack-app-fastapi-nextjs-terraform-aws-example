variable "main_domain" {
  type        = string
  description = "The domain name of the main website, e.g. example.com"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}
