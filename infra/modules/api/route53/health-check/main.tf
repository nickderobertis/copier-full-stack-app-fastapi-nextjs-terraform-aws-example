resource "aws_route53_health_check" "api" {
  fqdn              = var.api_fqdn
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health-check"
  failure_threshold = 3
  request_interval  = var.health_check_interval
  tags              = var.tags
}
