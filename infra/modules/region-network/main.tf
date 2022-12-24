module "acm" {
  source = "./acm"

  domain_name     = var.main_domain
  route53_zone_id = var.route53_zone_id
  tags            = var.tags
}
