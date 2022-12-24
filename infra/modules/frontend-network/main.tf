module "records" {
  source = "./records"

  route53_zone_id   = var.route53_zone_id
  route53_zone_name = var.route53_zone_name
  fe_subdomain      = var.fe_subdomain
  record_type       = var.record_type
}

module "healthcheck" {
  source = "./health-check"
  depends_on = [
    module.records
  ]

  web_fqdn              = var.fe_fqdn
  health_check_interval = var.health_check_interval
  tags                  = var.tags
}
