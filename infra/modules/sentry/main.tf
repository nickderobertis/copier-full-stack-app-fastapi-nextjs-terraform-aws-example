terraform {
  required_providers {
    sentry = {
      source = "jianyuan/sentry"
      version = "0.9.4"
    }
  }
}

data "sentry_organization" "this" {
  slug = var.sentry_organization_slug
}

resource "sentry_team" "this" {
  organization = data.sentry_organization.this.id
  name         = var.project_name
}

resource "sentry_project" "this" {
  organization = data.sentry_organization.this.id
  team         = sentry_team.this.id
  name         = var.project_name
  platform     = var.platform
}

data "sentry_key" "this" {
  organization = sentry_project.this.organization
  project      = sentry_project.this.id

  first = true
}