include "root" {
  path   = find_in_parent_folders()
  expose = true
}

terraform {
  source = "../../modules/secrets//."
}

locals {
  app_email_user       = get_env("APP_EMAIL_USER")
  app_email_password   = get_env("APP_EMAIL_PASSWORD")
  e2e_google_user      = get_env("E2E_GOOGLE_USER")
  e2e_google_password  = get_env("E2E_GOOGLE_PASSWORD")
  google_scopes        = get_env("GOOGLE_SCOPES")
  google_client_id     = get_env("GOOGLE_CLIENT_ID")
  google_client_secret = get_env("GOOGLE_CLIENT_SECRET")
  google_jwt_secret    = get_env("GOOGLE_JWT_SECRET")
  sentry_auth_token    = get_env("SENTRY_AUTH_TOKEN")
  slack_webhook_url    = get_env("SLACK_WEBHOOK_URL")
  slack_token          = get_env("SLACK_TOKEN")
  vercel_api_token     = get_env("VERCEL_API_TOKEN")
  // Unlike in the rest of terragrunt source, this is the global app name
  // rather than the one with env suffix
  global_app_name = get_env("GLOBAL_APP_NAME")
}

inputs = {
  secrets = {
    APP_EMAIL_USER       = local.app_email_user
    APP_EMAIL_PASSWORD   = local.app_email_password
    E2E_GOOGLE_USER      = local.e2e_google_user
    E2E_GOOGLE_PASSWORD  = local.e2e_google_password
    GOOGLE_CLIENT_ID     = local.google_client_id
    GOOGLE_CLIENT_SECRET = local.google_client_secret
    GOOGLE_JWT_SECRET    = local.google_jwt_secret
    SENTRY_AUTH_TOKEN    = local.sentry_auth_token
    SLACK_WEBHOOK_URL    = local.slack_webhook_url
    SLACK_TOKEN          = local.slack_token
    VERCEL_API_TOKEN     = local.vercel_api_token

  }
  params = {
    GOOGLE_SCOPES = local.google_scopes
  }
  app_name     = local.global_app_name
  service_name = "global"
}
