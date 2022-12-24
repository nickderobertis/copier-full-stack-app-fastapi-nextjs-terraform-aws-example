include "root" {
  path = find_in_parent_folders()
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/vpn.hcl"
}

dependency "network" {
  config_path = "../api/network"
}

locals {
  output_directory = abspath("${dirname(find_in_parent_folders())}/prod/generated")
}

inputs = {
  output_directory = local.output_directory
  vpc_id           = dependency.network.outputs.vpc_id
  subnet_id        = dependency.network.outputs.public_subnets[0]
}
