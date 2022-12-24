output "prometheus_workspace_arn" {
  description = "Amazon Resource Name (ARN) of the workspace"
  value       = module.prometheus.workspace_arn
}

output "prometheus_workspace_id" {
  description = "Identifier of the workspace"
  value       = module.prometheus.workspace_id
}

output "prometheus_workspace_prometheus_endpoint" {
  description = "Prometheus endpoint available for this workspace"
  value       = module.prometheus.workspace_prometheus_endpoint
}

output "monitoring_instance_ip" {
  value = module.ec2.instance_ip
}

output "private_key_file" {
  value = module.ec2.private_key_file
}

output "public_key_file" {
  value = module.ec2.public_key_file
}

output "connection_string" {
  value = module.ec2.connection_string
}

output "grafana_admin_password" {
  value = random_password.grafana_admin_password.result
  sensitive = true
}