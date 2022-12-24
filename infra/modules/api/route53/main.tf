module "records" {
  source = "./records"

  route53_zone_id   = var.route53_zone_id
  route53_zone_name = var.route53_zone_name
  lb_dns_name       = var.lb_dns_name
  api_record_name   = var.api_subdomain
}

module "healthcheck" {
  source = "./health-check"
  depends_on = [
    module.records
  ]

  api_fqdn              = var.api_fqdn
  health_check_interval = var.health_check_interval
  tags                  = var.tags
}
