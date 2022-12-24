output "names" {
  # Names are not sensitive
  value       = module.ssm.names
  description = "A list of all of the parameter names"
}

output "values" {
  description = "A list of all of the parameter values"
  value       = module.ssm.values
  sensitive   = true
}

output "map" {
  description = "A map of the names and values created"
  value       = module.ssm.map
  sensitive   = true
}

output "arn_map" {
  description = "A map of the names and ARNs created"
  value       = module.ssm.arn_map
}

output "env_arn_map" {
  description = "A map of the names and ARNs created, with the name in the format of ENV_VAR_NAME"
  value       = local.env_arn_map
}