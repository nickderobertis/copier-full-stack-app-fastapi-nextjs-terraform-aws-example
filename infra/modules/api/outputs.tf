output "service_name" {
  value = module.ecs.service_name
}

output "cluster_name" {
  value = module.ecs.cluster_name
}

output "full_image_name" {
  value = module.docker.full_image_name
}

output "container_name" {
  value = module.ecs.container_name
}

output "aws_region" {
  value = data.aws_region.current.name
}

output "ecr_repository_id" {
  value = module.ecr.repository_id
}

output "ecr_address" {
  value = module.docker.ecr_address
}

output "base_image_name" {
  value = "${module.docker.ecr_address}/${module.ecr.repository_id}"
}

output "task_definition_family" {
  value = module.ecs.task_definition_family
}

output "sentry_project_details" {
  value = module.sentry.project_details
}

output "sentry_team_id" {
  value = module.sentry.team_id
}

output "docker_file_sha" {
  value = module.docker.file_sha
}

output "secrets" {
  value = local.secrets
}

output "params" {
  value = local.params
}