
output "domain_name" {
  value = vercel_deployment.this.domains[0]
}

output "deployment_id" {
  value = vercel_deployment.this.id
}

output "project_id" {
  value = vercel_project.this.id
}