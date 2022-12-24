resource "aws_route53_health_check" "web" {
  fqdn              = var.web_fqdn
  port              = 443
  type              = "HTTPS"
  failure_threshold = 3
  request_interval  = var.health_check_interval
  tags              = var.tags
}
