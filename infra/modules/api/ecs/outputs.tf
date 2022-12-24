output "service_name" {
  value = aws_ecs_service.this.name
}

output "cluster_name" {
  value = module.ecs.cluster_name
}

output "container_name" {
  value = local.ecs_container_name
}

output "task_definition_family" {
  value = local.ecs_family
}