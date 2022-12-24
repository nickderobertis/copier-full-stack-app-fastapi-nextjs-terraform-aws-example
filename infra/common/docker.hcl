generate "ecr_data" {
  path      = "docker-ecr-data.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
locals {
  ecr_address = format("%v.dkr.ecr.%v.amazonaws.com", data.aws_caller_identity.this.account_id, data.aws_region.current.name)
}

data "aws_caller_identity" "this" {}
data "aws_region" "current" {}
data "aws_ecr_authorization_token" "token" {}
EOF
}

generate "docker_provider" {
  path      = "docker-provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "docker" {
  registry_auth {
    address  = local.ecr_address
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}
EOF
}