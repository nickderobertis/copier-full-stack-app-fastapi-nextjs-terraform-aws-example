locals {
  record_name = var.record_type == "A" ? "" : var.fe_subdomain
  # Vercel config, see
  # https://vercel.com/docs/concepts/projects/custom-domains#apex-domains  for A record and
  # https://vercel.com/docs/concepts/projects/custom-domains#subdomains   for CNAME record
  record_value = var.record_type == "A" ? "76.76.21.21" : "cname.vercel-dns.com"
}

module "main_record" {
  source = "../../records"

  zone_name = var.route53_zone_name
  zone_id   = var.route53_zone_id

  records = [
    {
      name    = local.record_name
      type    = var.record_type
      ttl     = 60
      records = [local.record_value]
    }
  ]
}


module "www_record" {
  source = "../../records"
  count  = var.record_type == "A" ? 1 : 0

  zone_name = var.route53_zone_name
  zone_id   = var.route53_zone_id

  records = [
    {
      name    = "www"
      type    = "CNAME"
      ttl     = 60
      records = ["cname.vercel-dns.com"]
    }
  ]
}
