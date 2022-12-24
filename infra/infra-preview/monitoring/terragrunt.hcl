include "root" {
  path = find_in_parent_folders()
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/monitoring.hcl"
}

include "docker" {
  path = "${dirname(find_in_parent_folders())}/common/docker.hcl"
}

locals {
  output_directory = abspath("${dirname(find_in_parent_folders())}/infra-preview/generated/monitoring")
}

inputs = {
  output_directory = local.output_directory
}
