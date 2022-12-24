dependency "global_network" {
  config_path = "../../global/network"
}

terraform {
  source = "../../modules//frontend-network"
}

inputs = {
  route53_zone_id   = dependency.global_network.outputs.route53_zone_id
  route53_zone_name = dependency.global_network.outputs.route53_zone_name
}


