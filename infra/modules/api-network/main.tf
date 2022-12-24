module "vpc" {
  source = "./vpc"

  app_name = var.app_name
  tags     = var.tags
}
