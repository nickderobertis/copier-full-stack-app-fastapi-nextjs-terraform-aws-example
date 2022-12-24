module "sg" {
  source  = "terraform-aws-modules/security-group/aws//."
  version = "4.13.0"

  name        = "${var.app_name}-db-sg"
  description = "PostgreSQL RDS security group"
  vpc_id      = var.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = var.vpc_cidr_block
    },
  ]

  tags = var.tags
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws//."
  version = "5.0.3"

  identifier           = "${var.app_name}-db"
  engine               = "postgres"
  engine_version       = "14.3"
  major_engine_version = "14"
  family               = "postgres14"
  # TODO: parameterize this section
  instance_class        = "db.t4g.micro"
  allocated_storage     = 10
  max_allocated_storage = 100
  db_name               = "appdb"
  username              = "app"
  multi_az              = false

  # TODO: adjust these for prod
  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false

  db_subnet_group_name   = var.db_subnet_group
  vpc_security_group_ids = [module.sg.security_group_id]

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  create_monitoring_role                = true
  monitoring_interval                   = 60
  monitoring_role_name                  = "${var.app_name}-db-mon-role"
  monitoring_role_use_name_prefix       = true
  monitoring_role_description           = "Monitoring role for ${var.app_name} database"

  parameters = [
    {
      name  = "autovacuum"
      value = 1
    },
    {
      name  = "client_encoding"
      value = "utf8"
    }
  ]
  tags = var.tags
}
