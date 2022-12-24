dependency "network" {
  config_path = "../api/network"
}

terraform {
  source = "../../modules/db//."
}


inputs = {
  db_subnet_group = dependency.network.outputs.db_subnet_group
  vpc_id          = dependency.network.outputs.vpc_id
  vpc_cidr_block  = dependency.network.outputs.vpc_cidr_block
}
