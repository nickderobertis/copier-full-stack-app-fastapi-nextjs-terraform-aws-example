terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.20.2"
    }
    sentry = {
      source = "jianyuan/sentry"
      version = "0.9.4"
    }
  }
}

locals {
  secrets = {}
  params = {
    SENTRY_API_PROJECT_SLUG = module.sentry.project_details.project
  }
}

module "sentry" {
  source = "../sentry"

  project_name = "${var.app_name}-api"
  sentry_organization_slug = var.sentry_organization_slug
  platform = "python"
}

module "ecr" {
  source = "../ecr"

  app_name = var.app_name
  tags     = var.tags
  service_name = "api"
}

module "docker" {
  source = "../docker"

  source_dir = var.api_source_dir
  ecr_id     = module.ecr.repository_id
  tags       = var.tags
}

module "lb_sg" {
  source = "./lb-sg"

  app_name = var.app_name
  vpc_id   = var.vpc_id
  tags     = var.tags
}

module "lb" {
  source = "./lb"

  app_name            = var.app_name
  app_short_name      = var.app_short_name
  vpc_id              = var.vpc_id
  public_subnets      = var.public_subnets
  security_group_id   = module.lb_sg.sg_id
  acm_certificate_arn = var.acm_certificate_arn
  tags                = var.tags
}

module "route53" {
  source = "./route53"

  api_subdomain         = var.api_subdomain
  api_fqdn              = var.api_fqdn
  health_check_interval = var.health_check_interval
  lb_dns_name           = module.lb.lb_dns_name
  route53_zone_id       = var.route53_zone_id
  route53_zone_name     = var.route53_zone_name
  tags                  = var.tags
}


module "ecs" {
  source = "./ecs"

  app_name      = var.app_name
  environment   = var.environment
  cpu           = var.cpu
  memory        = var.memory
  desired_count = var.desired_count

  vpc_id                    = var.vpc_id
  lb_sg_id                  = module.lb_sg.sg_id
  private_subnets           = var.private_subnets
  target_group_arn          = module.lb.target_group_arns[0]
  docker_image_name         = module.docker.full_image_name
  sentry_dsn                = module.sentry.project_details.dsn_secret
  enable_dev_endpoints      = var.enable_dev_endpoints
  db_host                   = var.db_host
  db_port                   = var.db_port
  db_user                   = var.db_user
  db_password               = var.db_password
  env_arn_map               = var.env_arn_map
  aws_region                = var.aws_region

  tags = var.tags
}
