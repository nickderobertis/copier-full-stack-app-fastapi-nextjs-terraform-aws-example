module "records" {
  source = "../../../records"

  zone_name = var.route53_zone_name
  zone_id   = var.route53_zone_id

  records = [
    {
      name    = var.api_record_name
      type    = "CNAME"
      ttl     = 60
      records = [var.lb_dns_name]
    }
  ]
}
