variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the certificate in"
}

variable "domain_name" {
  type = string
}

variable "tags" {
  type = map(string)
}
