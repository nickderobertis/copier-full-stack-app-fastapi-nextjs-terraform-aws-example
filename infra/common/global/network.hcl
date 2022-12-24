locals {
  domain_name = get_env("NETWORK_DOMAIN_NAME")
}

terraform {
  source = "../../modules//global-network"
}

inputs = {
  main_domain = local.domain_name
}


