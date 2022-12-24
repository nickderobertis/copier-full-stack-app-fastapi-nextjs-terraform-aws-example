data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws//."
  version = "3.14.2"
  name    = "${var.app_name}-vpc"
  cidr    = "10.0.0.0/16"

  azs              = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24"]
  database_subnets = ["10.0.201.0/24", "10.0.202.0/24"]

  enable_nat_gateway = true
  enable_dns_hostnames = true
  enable_vpn_gateway = false

  create_database_subnet_group       = true
  create_database_subnet_route_table = true

  tags = var.tags
}
