include "root" {
  path = find_in_parent_folders()
  expose = true
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/api/api.hcl"
}

include "persistent" {
  path = "${dirname(find_in_parent_folders())}/common/api/api-persistent-env.hcl"
}

include "docker" {
  path = "${dirname(find_in_parent_folders())}/common/docker.hcl"
}

dependency "region_network" {
  config_path = "../../../global/regions/${include.root.locals.aws_region}/network"
}

inputs = {
  acm_certificate_arn  = dependency.region_network.outputs.acm_certificate_arn
}
