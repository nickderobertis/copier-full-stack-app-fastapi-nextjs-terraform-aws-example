locals {
  sentry_project_slug = "${var.app_name}-web"
}

module "sentry" {
  source = "../sentry"

  project_name             = local.sentry_project_slug
  sentry_organization_slug = var.sentry_organization_slug
  platform                 = "javascript"
}

module "vercel" {
  source                   = "./vercel"
  project_name             = var.project_name
  project_directory        = var.project_directory
  api_url                  = var.api_url
  domain_name              = var.domain_name
  sentry_client_dsn        = module.sentry.project_details.dsn_public
  sentry_server_dsn        = module.sentry.project_details.dsn_secret
  sentry_project_slug      = local.sentry_project_slug
  sentry_auth_token        = var.sentry_auth_token
  sentry_organization_slug = var.sentry_organization_slug
  enable_dev_pages         = var.enable_dev_endpoints
  google_scopes            = var.google_scopes
}

