
variable "project_directory" {
  type        = string
  description = "The directory where the Vercel project to deploy is located"
}

variable "project_name" {
  type        = string
  description = "Name of the project in Vercel"
}

variable "api_url" {
  type        = string
  description = "The URL of the API"
}

variable "domain_name" {
  type        = string
  description = "The domain name to associate with the project"
}

variable "sentry_client_dsn" {
  type = string
}

variable "sentry_server_dsn" {
  type = string
}

variable "sentry_auth_token" {
  type = string
}

variable "sentry_project_slug" {
  type = string
}

variable "sentry_organization_slug" {
  type = string
}

variable "enable_dev_pages" {
  type    = bool
  default = false
}

variable "google_scopes" {
  type = string
}
