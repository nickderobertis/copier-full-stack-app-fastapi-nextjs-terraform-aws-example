locals {
  email_user     = get_env("APP_EMAIL_USER")
  email_password = get_env("APP_EMAIL_PASSWORD")
  sentry_organization_slug = get_env("SENTRY_ORGANIZATION_SLUG")
  sentry_auth_token = get_env("SENTRY_AUTH_TOKEN")
}

terraform {
  source = "../../modules/secrets//."
}

inputs = {
  secrets = {
    EMAIL_USER     = local.email_user
    EMAIL_PASSWORD = local.email_password
    SENTRY_AUTH_TOKEN = local.sentry_auth_token
  }
  params = {
    SENTRY_ORGANIZATION_SLUG = local.sentry_organization_slug
  }
}


