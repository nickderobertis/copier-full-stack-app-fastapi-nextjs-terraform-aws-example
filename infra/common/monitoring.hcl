terraform {
  source = "../../modules//monitoring"
}

dependency "api_network" {
  config_path = "../api/network"
}

dependency "global_network" {
  config_path = "../../global/network"
}

generate "slack_provider" {
  path      = "slack-provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "slack" {}
EOF
}

locals {
  project_root               = abspath("${get_terragrunt_dir()}/../../..")
  grafana_directory          = "${local.project_root}/grafana"
  network_exporter_directory = "${local.project_root}/network-exporter"
  prometheus_directory       = "${local.project_root}/prometheus"
  docker_compose_contents    = run_cmd("--terragrunt-quiet", "../../scripts/internal/get-monitoring-compose-contents.sh")
}

inputs = {
  vpc_id                     = dependency.api_network.outputs.vpc_id
  subnet_id                  = dependency.api_network.outputs.public_subnets[0]
  grafana_directory          = local.grafana_directory
  network_exporter_directory = local.network_exporter_directory
  prometheus_directory       = local.prometheus_directory
  docker_compose_contents    = local.docker_compose_contents
  route53_zone_id            = dependency.global_network.outputs.route53_zone_id
  route53_zone_name          = dependency.global_network.outputs.route53_zone_name
}
