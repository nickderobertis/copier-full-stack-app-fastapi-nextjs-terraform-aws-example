module "zones" {
  source = "./zones"

  main_domain = var.main_domain
  tags        = var.tags
}
