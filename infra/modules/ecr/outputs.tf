output "repository_id" {
  description = "The ID of the repository"
  value       = module.ecr.repository_id
}

output "repository_arn" {
  description = "Full ARN of the repository"
  value       = module.ecr.repository_arn
}