terraform {
  required_providers {
    vercel = {
      source  = "vercel/vercel"
      version = "~> 0.8"
    }
  }
}

data "vercel_project_directory" "this" {
  path = var.project_directory
}

resource "vercel_project" "this" {
  name      = var.project_name
  framework = "nextjs"

  environment = [
    {
      key    = "NEXT_PUBLIC_API_URL"
      value  = var.api_url
      target = ["production", "preview"]
    },
    {
      key    = "NEXT_PUBLIC_SENTRY_DSN"
      value  = var.sentry_client_dsn
      target = ["production", "preview"]
    },
    {
      key    = "SENTRY_SERVER_DSN"
      value  = var.sentry_server_dsn
      target = ["production", "preview"]
    },
    {
      key    = "SENTRY_AUTH_TOKEN"
      value  = var.sentry_auth_token
      target = ["production", "preview"]
    },
    {
      key    = "SENTRY_ORG"
      value  = var.sentry_organization_slug
      target = ["production", "preview"]
    },
    {
      key    = "SENTRY_PROJECT"
      value  = var.sentry_project_slug
      target = ["production", "preview"]
    },
    {
      key    = "SENTRY_URL"
      value  = "https://sentry.io/"
      target = ["production", "preview"]
    },
    {
      key    = "NEXT_PUBLIC_ENABLE_DEV_PAGES"
      value  = tostring(var.enable_dev_pages)
      target = ["production", "preview"]
    },
    {
      key    = "NEXT_PUBLIC_GOOGLE_SCOPES"
      value  = var.google_scopes
      target = ["production", "preview"]
    },
  ]
}

resource "vercel_deployment" "this" {
  project_id  = vercel_project.this.id
  files       = data.vercel_project_directory.this.files
  path_prefix = var.project_directory
  production  = true
}

resource "vercel_project_domain" "this" {
  project_id = vercel_project.this.id
  domain     = var.domain_name
}
