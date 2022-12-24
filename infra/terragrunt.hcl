locals {
  global_app_name          = get_env("GLOBAL_APP_NAME")
  main_domain              = get_env("NETWORK_DOMAIN_NAME")
  sentry_organization_slug = get_env("SENTRY_ORGANIZATION_SLUG")
  slack_webhook_url        = get_env("SLACK_WEBHOOK_URL")
  environment_vars         = read_terragrunt_config(find_in_parent_folders("env.hcl"))
  region_vars              = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  environment = local.environment_vars.locals.environment
  subdomain   = local.environment_vars.locals.subdomain
  name_suffix = local.environment_vars.locals.name_suffix
  aws_region  = local.region_vars.locals.aws_region

  full_app_name          = "${local.global_app_name}-${local.name_suffix}"
  api_name               = "api"
  api_maindomain         = "${local.api_name}.${local.main_domain}"
  api_subdomain          = local.subdomain == "" ? local.api_name : "${local.api_name}-${local.subdomain}"
  monitoring_name        = "monitoring"
  monitoring_maindomain  = "${local.monitoring_name}.${local.main_domain}"
  monitoring_subdomain   = local.subdomain == "" ? local.monitoring_name : "${local.monitoring_name}-${local.subdomain}"
  fe_fqdn                = local.subdomain == "" ? local.main_domain : "${local.subdomain}.${local.main_domain}"
  fe_url                 = "https://${local.fe_fqdn}"
  api_fqdn               = local.subdomain == "" ? local.api_maindomain : "${local.api_subdomain}.${local.main_domain}"
  api_url                = "https://${local.api_fqdn}"
  api_record_name        = local.subdomain == "" ? local.api_name : local.api_subdomain
  monitoring_fqdn        = local.subdomain == "" ? local.monitoring_maindomain : "${local.monitoring_subdomain}.${local.main_domain}"
  monitoring_url         = "https://${local.monitoring_fqdn}"
  monitoring_record_name = local.subdomain == "" ? local.monitoring_name : local.monitoring_subdomain
  slack_channel          = "${local.full_app_name}-monitoring"


  # Set up remote state key so that it is the same across preview deployments, but otherwise unique
  relative_include_path                   = path_relative_to_include()
  relative_include_path_without_first_dir = replace(local.relative_include_path, "/^[^/]+//", "")
  relative_first_dir                      = replace(local.relative_include_path, "//.*/", "")
  is_preview_dir                          = local.relative_first_dir == "api-preview" || local.relative_first_dir == "infra-preview"
  remote_state_key_base                   = local.is_preview_dir ? "preview/${local.relative_include_path_without_first_dir}" : local.relative_include_path

  # Enable dev endpoints when not a prod deploy
  enable_dev_endpoints = local.relative_first_dir == "prod" ? false : true

  tags = {
    Environment = local.environment
    Project     = local.full_app_name
  }
}

# Indicate what region to deploy the resources into
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.aws_region}"
}
EOF
}

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "${local.full_app_name}-terraform-state"

    key            = "${local.remote_state_key_base}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "${local.full_app_name}-lock-table"
  }
}

inputs = merge(
  {
    app_name                 = local.full_app_name
    tags                     = local.tags
    environment              = local.environment
    aws_region               = local.aws_region
    subdomain                = local.subdomain
    fe_subdomain             = local.subdomain
    main_domain              = local.main_domain
    fe_fqdn                  = local.fe_fqdn
    fe_domain                = local.fe_fqdn
    fe_url                   = local.fe_url
    api_fqdn                 = local.api_fqdn
    api_subdomain            = local.api_subdomain
    api_url                  = local.api_url
    api_record_name          = local.api_record_name
    monitoring_fqdn          = local.monitoring_fqdn
    monitoring_subdomain     = local.monitoring_subdomain
    monitoring_url           = local.monitoring_url
    monitoring_record_name   = local.monitoring_record_name
    enable_dev_endpoints     = local.enable_dev_endpoints
    sentry_organization_slug = local.sentry_organization_slug
    slack_webhook_url        = local.slack_webhook_url
    slack_channel            = local.slack_channel
  },
  local.environment_vars.inputs
)
