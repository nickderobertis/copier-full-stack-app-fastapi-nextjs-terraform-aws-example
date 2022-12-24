dependency "api_network" {
  config_path = "../network"
}

dependency "db" {
  config_path = "../../db"
}

dependency "secrets" {
  config_path = "../../secrets"
}

dependency "global-secrets" {
  config_path = "../../../global/secrets"
}

inputs = {
  vpc_id          = dependency.api_network.outputs.vpc_id
  public_subnets  = dependency.api_network.outputs.public_subnets
  private_subnets = dependency.api_network.outputs.private_subnets
  db_host         = dependency.db.outputs.db_host
  db_port         = dependency.db.outputs.db_port
  db_user         = dependency.db.outputs.db_user
  db_password     = dependency.db.outputs.db_password
  env_arn_map     = merge(dependency.secrets.outputs.env_arn_map, dependency.global-secrets.outputs.env_arn_map)
}
