
resource "aws_cloudwatch_log_group" "this" {
  name = "/aws/vendedlogs/${var.app_name}/aws-managed-prometheus"

  tags = var.tags
}

module "prometheus" {
  source  = "terraform-aws-modules/managed-service-prometheus/aws"
  version = "2.2.0"

  workspace_alias = var.app_name

  alert_manager_definition = <<-EOT
  alertmanager_config: |
    route:
      receiver: 'default'
    receivers:
      - name: 'default'
        sns_configs:
        - topic_arn: ${var.sns_topic_arn}
          sigv4:
            region: ${var.aws_region}
  EOT

  rule_group_namespaces = {
    temp = {
      name = "${var.app_name}-01"
      data = <<-EOT
      groups:
        - name: Alerts
          rules:
          - alert: APILoadBalancerFailedHealthCheck
            # TODO: parameterize and make match expected count
            expr: min(aws_alb_healthy_host_count_average{}) < 1
            for: 1m
            labels:
              severity: page
            annotations:
              summary: API Load Balancer failed health check
          - alert: Route53FailedHealthCheck
            expr: min(aws_route53_health_check_status_average{}) < 1
            for: 1m
            labels:
              severity: page
            annotations:
              summary: Route53 failed health check - URL is down
      EOT
    }
  }

  tags = var.tags
}

resource "null_resource" "attach_log_group" {
  // TODO: Remove this once aws provider supports attaching log group to prometheus
  provisioner "local-exec" {
    command = "aws amp create-logging-configuration --workspace-id ${module.prometheus.workspace_id} --log-group-arn \"${aws_cloudwatch_log_group.this.arn}:*\" --region ${var.aws_region}"
  }

}
