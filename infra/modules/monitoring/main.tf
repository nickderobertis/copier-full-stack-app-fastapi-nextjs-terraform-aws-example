terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.20.2"
    }
    slack = {
      source  = "pablovarela/slack"
      version = "~> 1.1"
    }
  }
}

locals {
  monitoring_instance_name = "${var.app_name}-monitoring"
}

resource "slack_conversation" "this" {
  name                   = var.slack_channel
  topic                  = "Monitoring for ${var.app_name}"
  is_private             = false
  adopt_existing_channel = true
}

module "notify_slack" {
  source  = "terraform-aws-modules/notify-slack/aws"
  version = "~> 5.3"

  sns_topic_name       = "${var.app_name}-monitoring"
  iam_role_name_prefix = "${var.app_name}-monitoring"

  slack_webhook_url = var.slack_webhook_url
  slack_channel     = var.slack_channel
  slack_username    = "${var.app_name}-monitoring"
}

resource "aws_sns_topic_policy" "default" {
  arn = module.notify_slack.slack_topic_arn

  policy = data.aws_iam_policy_document.sns_topic_policy.json
}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "sns_topic_policy" {
  policy_id = "__default_policy_ID"

  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceAccount"

      values = [
        data.aws_caller_identity.current.account_id,
      ]
    }

    condition {
      test     = "ArnEquals"
      variable = "AWS:SourceArn"

      values = [
        module.prometheus.workspace_arn,
      ]
    }

    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["aps.amazonaws.com"]
    }

    resources = [
      module.notify_slack.slack_topic_arn,
    ]

    sid = "Allow_Publish_Alarms"
  }
}

module "prometheus" {
  source = "../prometheus"

  app_name      = var.app_name
  tags          = var.tags
  sns_topic_arn = module.notify_slack.slack_topic_arn
  aws_region    = data.aws_region.current.name
}

resource "aws_security_group" "monitoring" {
  name        = local.monitoring_instance_name
  description = "Security group for monitoring server ${local.monitoring_instance_name}"
  vpc_id      = var.vpc_id

  # For prometheus to access cloudwatch exporter
  ingress {
    protocol  = "tcp"
    from_port = 5000
    to_port   = 5000
    # TODO: restrict so only prometheus can access
    cidr_blocks = ["0.0.0.0/0"]
  }

  # For user Grafana access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = var.tags
}


module "ecr_grafana" {
  source = "../ecr"

  app_name     = var.app_name
  tags         = var.tags
  service_name = "grafana"
}


module "docker_grafana" {
  source = "../docker"

  source_dir = var.grafana_directory
  ecr_id     = module.ecr_grafana.repository_id
  tags       = var.tags
  build_args = {
    APP_NAME    = var.app_name
    DOMAIN_NAME = var.monitoring_fqdn
  }
}

module "ecr_network_exporter" {
  source = "../ecr"

  app_name     = var.app_name
  tags         = var.tags
  service_name = "network-exporter"
}


module "docker_network_exporter" {
  source = "../docker"

  source_dir = var.network_exporter_directory
  ecr_id     = module.ecr_network_exporter.repository_id
  tags       = var.tags
  build_args = {
    AWS_DEFAULT_REGION = data.aws_region.current.name
    APP_NAME           = var.app_name
  }
}

module "ecr_prometheus" {
  source = "../ecr"

  app_name     = var.app_name
  tags         = var.tags
  service_name = "prometheus"
}


module "docker_prometheus" {
  source = "../docker"

  source_dir = var.prometheus_directory
  ecr_id     = module.ecr_prometheus.repository_id
  tags       = var.tags
  build_args = {
    CLOUDWATCH_EXPORTER_URL_NO_SCHEME = "${var.monitoring_fqdn}:5000"
    AWS_DEFAULT_REGION                = data.aws_region.current.name
    PROMETHEUS_URL                    = module.prometheus.workspace_prometheus_endpoint
  }
}

module "ec2_ecr_role" {
  source = "../ec2-ecr-role"

  app_name = var.app_name
  tags     = var.tags
  ecr_arns = [
    module.ecr_grafana.repository_arn,
    module.ecr_network_exporter.repository_arn,
    module.ecr_prometheus.repository_arn,
  ]
  extra_global_permissions = [
    # Note: The following permissions are split into sections so that later
    # when services are scaled out into separate servers, can split up the permissions.
    # In some cases, multiple services request the same permisssion, in which case
    # it is commented out in all but one of the requesting services.

    # Add permissions for prometheus access from Grafana
    "aps:ListWorkspaces",
    "aps:DescribeWorkspace",
    "aps:QueryMetrics",
    "aps:GetLabels",
    "aps:GetSeries",
    "aps:GetMetricMetadata",

    # Add permissions for Clouwatch metrics/logs direct access from Grafana
    # "cloudwatch:DescribeAlarmsForMetric",
    # "cloudwatch:DescribeAlarmHistory",
    # "cloudwatch:DescribeAlarms",
    "cloudwatch:ListMetrics",
    "cloudwatch:GetMetricData",
    "cloudwatch:GetInsightRuleReport",
    "logs:DescribeLogGroups",
    "logs:GetLogGroupFields",
    "logs:StartQuery",
    "logs:StopQuery",
    "logs:GetQueryResults",
    "logs:GetLogEvents",
    "ec2:DescribeTags",
    "ec2:DescribeInstances",
    "ec2:DescribeRegions",
    "tag:GetResources",


    # Add permisssions for remote prometheus access from prometheus container
    "aps:RemoteWrite",

    # Add permissions for cloudwatch exporter access
    "tag:GetResources",
    # "cloudwatch:GetMetricData",
    # "cloudwatch:ListMetrics",
    # "cloudwatch:GetMetricStatistics",
    "cloudwatch:Describe*",

    # Add permissions for all docker containers to create logs
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:PutLogEvents",
  ]
}

resource "random_password" "grafana_admin_password" {
  length  = 16
  special = true
}

module "secrets" {
  source = "../secrets"

  app_name     = var.app_name
  tags         = var.tags
  service_name = "monitoring"
  params = {
    DOCKER_REGISTRY      = module.docker_grafana.ecr_address
    GRAFANA_TAG          = module.docker_grafana.file_sha
    NETWORK_EXPORTER_TAG = module.docker_network_exporter.file_sha
    PROMETHEUS_TAG       = module.docker_prometheus.file_sha
    GRAFANA_URL          = var.monitoring_url
  }
  secrets = {
    GRAFANA_PASSWORD      = random_password.grafana_admin_password.result
    PROMETHEUS_URL        = module.prometheus.workspace_prometheus_endpoint
    PROMETHEUS_AWS_REGION = data.aws_region.current.name
  }
}

module "ec2" {
  source = "../ec2"
  depends_on = [
    module.secrets
  ]

  startup_script = <<EOT
set -ex
# TODO: move these one-time setup commdands to a custom AMI
sudo yum update -y
sudo amazon-linux-extras install docker -y
sudo yum install jq -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo curl -L https://github.com/docker/compose/releases/download/v2.10.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# TODO: replace with real docker pull/compose start
# Hard-coded env vars from script generation
export APP_NAME=${var.app_name}
export AWS_DEFAULT_REGION=${data.aws_region.current.name}

# Get other env vars from SSM
get_parameter_store_tags() {
    echo $(aws ssm get-parameters-by-path --with-decryption --path /$APP_NAME/monitoring  --region $AWS_DEFAULT_REGION)
}

params_to_env () {
    params=$1

    # If .Tags does not exist we assume ssm Parameteres object.
    SELECTOR="Name"

    for key in $(echo $params | /usr/bin/jq -r ".[][].$${SELECTOR}"); do
                value=$(echo $params | /usr/bin/jq -r ".[][] | select(.$${SELECTOR}==\"$key\") | .Value")
                key=$(echo "$${key##*/}" | /usr/bin/tr ':' '_' | /usr/bin/tr '-' '_' | /usr/bin/tr '[:lower:]' '[:upper:]')
                export $key="$value"
                echo "$key=$value"
    done
}
TAGS=$(get_parameter_store_tags)
params_to_env "$TAGS"

cd /home/ec2-user
cat >docker-compose.yml << 'EOL'
${var.docker_compose_contents}
EOL

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $DOCKER_REGISTRY
docker-compose up -d
    EOT

  app_name             = var.app_name
  instance_type        = var.monitoring_instance_type
  output_directory     = var.output_directory
  instance_name        = local.monitoring_instance_name
  security_group_ids   = [aws_security_group.monitoring.id]
  vpc_id               = var.vpc_id
  subnet_id            = var.subnet_id
  iam_instance_profile = module.ec2_ecr_role.iam_instance_profile
  tags                 = var.tags
}

module "record" {
  source = "../records"

  zone_name = var.route53_zone_name
  zone_id   = var.route53_zone_id

  records = [
    {
      name    = var.monitoring_record_name
      type    = "CNAME"
      ttl     = 60
      records = [module.ec2.public_dns]
    }
  ]
}

