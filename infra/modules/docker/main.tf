terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.20.2"
    }
  }
}

locals {
  file_sha    = sha1(join("", [for f in fileset(local.src_dir, "**") : filesha1("${local.src_dir}/${f}")]))
  image_name  = "${var.ecr_id}:${local.file_sha}"
  src_dir     = var.source_dir
  ecr_address = format("%v.dkr.ecr.%v.amazonaws.com", data.aws_caller_identity.this.account_id, data.aws_region.current.name)
  ecr_image   = format("%v/%v", local.ecr_address, local.image_name)
}

data "aws_caller_identity" "this" {}
data "aws_region" "current" {}
data "aws_ecr_authorization_token" "token" {}

resource "docker_image" "this" {
  name = local.ecr_image
  build {
    path = local.src_dir
    build_arg = var.build_args
  }
  triggers = {
    dir_sha1 = local.file_sha
  }
}

resource "docker_registry_image" "this" {
  name = docker_image.this.name
}
