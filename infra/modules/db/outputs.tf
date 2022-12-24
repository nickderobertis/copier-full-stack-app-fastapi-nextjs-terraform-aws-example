output "db_host" {
  value = module.rds.db_instance_endpoint
}

output "db_port" {
  value = module.rds.db_instance_port
}

output "db_user" {
  value     = module.rds.db_instance_username
  sensitive = true
}

output "db_password" {
  value     = module.rds.db_instance_password
  sensitive = true
}
