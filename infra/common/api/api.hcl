dependency "global_network" {
  config_path = "../../../global/network"
}

generate "sentry_provider" {
  path      = "sentry-provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "sentry" {}
EOF
}

locals {
  app_short_name    = get_env("APP_SHORT_NAME")
  project_directory = abspath("${get_terragrunt_dir()}/../../../../backend")
}

terraform {
  source = "../../../modules//api"
}


inputs = {
  app_short_name            = local.app_short_name
  api_source_dir            = local.project_directory
  route53_zone_id           = dependency.global_network.outputs.route53_zone_id
  route53_zone_name         = dependency.global_network.outputs.route53_zone_name
}
