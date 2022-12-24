locals {
  project_directory = abspath("${get_terragrunt_dir()}/../../../frontend/app-example")
  sentry_auth_token = get_env("SENTRY_AUTH_TOKEN")
  google_scopes     = get_env("GOOGLE_SCOPES")
}

terraform {
  source = "../../modules//frontend"
}

inputs = {
  project_directory = local.project_directory
  sentry_auth_token = local.sentry_auth_token
  google_scopes     = local.google_scopes
}
