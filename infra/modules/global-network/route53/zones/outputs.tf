output "route53_zone_id" {
  value = module.zones.route53_zone_zone_id[keys(module.zones.route53_zone_zone_id)[0]]
}

output "route53_zone_name" {
  value = keys(module.zones.route53_zone_zone_id)[0]
}
