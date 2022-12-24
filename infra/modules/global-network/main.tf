module "route53" {
  source = "./route53"

  main_domain = var.main_domain
  tags        = var.tags
}
