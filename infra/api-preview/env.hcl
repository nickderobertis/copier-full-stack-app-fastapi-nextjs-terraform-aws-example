locals {
  environment = "staging"
  subdomain   = get_env("NETWORK_STAGING_SUBDOMAIN")
  name_suffix = get_env("APP_STAGING_NAME_SUFFIX")
}
