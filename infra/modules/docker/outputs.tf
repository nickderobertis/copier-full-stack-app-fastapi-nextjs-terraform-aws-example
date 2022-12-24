output "sha" {
  value = docker_registry_image.this.sha256_digest
}

output "id" {
  value = docker_registry_image.this.id
}

output "full_image_name" {
  value = docker_registry_image.this.name
}

output "image_name" {
  value = local.image_name
}

output "ecr_address" {
  value = local.ecr_address
}

output "file_sha" {
  value = local.file_sha
}