include "root" {
  path   = find_in_parent_folders()
  expose = true
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/api/api.hcl"
}

include "docker" {
  path = "${dirname(find_in_parent_folders())}/common/docker.hcl"
}

dependency "region_network" {
  config_path = "../../../global/regions/${include.root.locals.aws_region}/network"
}

dependency "api_network" {
  config_path = "../../../staging/api/network"
}

dependency "db" {
  config_path = "../../../staging/db"
}

dependency "secrets" {
  config_path = "../../../staging/secrets"
}

dependency "global-secrets" {
  config_path = "../../../global/secrets"
}

inputs = {
  acm_certificate_arn = dependency.region_network.outputs.acm_certificate_arn
  vpc_id              = dependency.api_network.outputs.vpc_id
  public_subnets      = dependency.api_network.outputs.public_subnets
  private_subnets     = dependency.api_network.outputs.private_subnets
  db_host             = dependency.db.outputs.db_host
  db_port             = dependency.db.outputs.db_port
  db_user             = dependency.db.outputs.db_user
  db_password         = dependency.db.outputs.db_password
  env_arn_map         = merge(dependency.secrets.outputs.env_arn_map, dependency.global-secrets.outputs.env_arn_map)
}
