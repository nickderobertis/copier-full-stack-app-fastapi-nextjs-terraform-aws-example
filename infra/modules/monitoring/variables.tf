variable "app_name" {
    type        = string
    description = "The name of the application"
}

variable "monitoring_instance_type" {
  description = "The instance type to use for the monitoring server (Grafana + network-based exporters)"
  default     = "t2.micro"
}

variable "output_directory" {
  description = "The name of the directory to download the keys to"
  default     = "generated"
}

variable "vpc_id" {
    description = "The ID of the VPC to create the monitoring server in"
    type        = string
}

variable "subnet_id" {
  type        = string
  description = "ID of AWS subnet to put the monitoring instance in. Should be in the same VPC matching the passed vpc_id"
}

variable "tags" {
  type        = map(string)
  description = "The tags to apply to the resources"
}

variable "grafana_directory" {
  type        = string
  description = "The directory that contains the source for the Grafana container"
}

variable "network_exporter_directory" {
  type        = string
  description = "The directory that contains the source for the network exporter container"
}

variable "prometheus_directory" {
  type        = string
  description = "The directory that contains the source for the Prometheus container"
}

variable "docker_compose_contents" {
  type        = string
  description = "The contents of the docker-compose.yml file to use for the monitoring server"
}

variable "monitoring_fqdn" {
  type        = string
  description = "The fully qualified domain name to use for the monitoring server, e.g. monitoring.example.com"
}

variable "monitoring_url" {
  type        = string
  description = "The URL to use for the monitoring server, e.g. https://monitoring.example.com"
}

variable "monitoring_record_name" {
  type        = string
  description = "The name of the DNS record to create for the monitoring server, e.g. monitoring"
}

variable "route53_zone_id" {
  type        = string
  description = "The ID of the Route53 zone to create the records in"
}

variable "route53_zone_name" {
  type        = string
  description = "The name of the Route53 zone to create the records in"
}

variable "slack_webhook_url" {
  type        = string
  description = "The Slack API URL to use for sending alerts to Slack"
  sensitive = true
}

variable "slack_channel" {
  type        = string
  description = "The Slack channel to send alerts to"
}