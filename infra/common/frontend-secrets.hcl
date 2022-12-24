locals {
  project_directory = abspath("${get_terragrunt_dir()}/../../../frontend/copier-full-stack-app-fastapi-nextjs-terraform-aws-example")
  sentry_auth_token = get_env("SENTRY_AUTH_TOKEN")
}

terraform {
  source = "../../modules//secrets"
}

dependency "frontend" {
  config_path = "../frontend"
}

inputs = {
  params = {
    SENTRY_FE_PROJECT_SLUG = dependency.frontend.outputs.sentry_project_details.project
  }
}
