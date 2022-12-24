terraform {
  source = "../../../../modules//region-network"
}

dependency "global_network" {
  config_path = "../../../network"
}

inputs = {
  route53_zone_id = dependency.global_network.outputs.route53_zone_id
}
