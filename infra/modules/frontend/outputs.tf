
output "domain_name" {
  value = module.vercel.domain_name
}

output "vercel_deployment_id" {
  value = module.vercel.deployment_id
}

output "vercel_project_id" {
  value = module.vercel.project_id
}

output "sentry_project_details" {
  value = module.sentry.project_details
}

output "sentry_team_id" {
  value = module.sentry.team_id
}
