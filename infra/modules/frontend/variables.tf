
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

variable "is_primary_domain" {
  type        = bool
  description = "Whether the domain is the primary domain for the project"
  default     = false
}

variable "app_name" {
  type = string
}

variable "sentry_organization_slug" {
  type = string
}

variable "sentry_auth_token" {
  type = string
}

variable "enable_dev_endpoints" {
  type    = bool
  default = false
}


variable "google_scopes" {
  type = string
}
