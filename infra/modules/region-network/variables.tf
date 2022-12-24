variable "main_domain" {
  type        = string
  description = "The domain name of the main website, e.g. example.com"
}

variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the certificate in"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}
