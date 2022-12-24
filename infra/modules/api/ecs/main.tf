locals {
  cloudwatch_log_group_name                 = "/aws/ecs/${var.app_name}"
  ecs_family                                = "${var.app_name}-ecs-family"
  task_iam_role_name                        = "${var.app_name}-task-role"
  task_iam_policy_name                      = "${var.app_name}-task-policy"
  task_iam_policy_attachment_name           = "${var.app_name}-task-policy-attachment"
  task_iam_execution_role_name              = "${var.app_name}-task-ex-role"
  task_iam_execution_policy_name            = "${var.app_name}-task-ex-policy"
  task_iam_execution_policy_attachment_name = "${var.app_name}-task-ex-policy-attachment"
  service_name                              = "${var.app_name}-service"
  task_sg_name                              = "${var.app_name}-task-sg"
  ecs_container_name                        = "${var.app_name}-container"
}

module "ecs" {
  source  = "terraform-aws-modules/ecs/aws//."
  version = "4.1.1"

  cluster_name = "${var.app_name}-ecs"

  cluster_configuration = {
    execute_command_configuration = {
      logging = "OVERRIDE"
      log_configuration = {
        cloud_watch_log_group_name = local.cloudwatch_log_group_name
      }
    }
  }

  fargate_capacity_providers = {
    FARGATE = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
    FARGATE_SPOT = {
      default_capacity_provider_strategy = {
        weight = 50
      }
    }
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/ecs/${local.cloudwatch_log_group_name}"
  retention_in_days = 7

  tags = var.tags
}

resource "aws_iam_role" "task_role" {
  name = local.task_iam_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = ["ecs-tasks.amazonaws.com"]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags = var.tags
}

resource "aws_iam_policy" "task_policy" {
  name = local.task_iam_policy_name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:DescribeLogGroups"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogStream",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "task_policy_attachment" {
  policy_arn = aws_iam_policy.task_policy.arn
  role       = local.task_iam_role_name
}

resource "aws_iam_role" "task_execution_role" {
  name = local.task_iam_execution_role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = ["ecs-tasks.amazonaws.com"]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
  tags = var.tags
}

resource "aws_iam_policy" "task_execution_policy" {
  name = local.task_iam_execution_policy_name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "logs:CreateLogStream",
          "logs:CreateLogGroup",
          "logs:PutLogEvents",
          "ssm:GetParameters"
        ],
        Resource = "*"
      }
    ]
  })
  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "task_execution_policy_attachment" {
  policy_arn = aws_iam_policy.task_execution_policy.arn
  role       = local.task_iam_execution_role_name
}

resource "aws_ecs_task_definition" "service" {
  family                   = local.ecs_family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.task_role.arn
  cpu                      = var.cpu
  memory                   = var.memory
  container_definitions = jsonencode([
    {
      essential = true
      image     = var.docker_image_name
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "${aws_cloudwatch_log_group.this.name}"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      healthCheck = {
        retries     = 3
        command     = ["CMD-SHELL", "curl -f localhost:8001/health-check || exit 1"]
        timeout     = 5
        interval    = 30
        startPeriod = null
      }
      name = local.ecs_container_name
      portMappings = [
        {
          containerPort = 8001
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "DB_HOST"
          value = var.db_host
        },
        {
          name  = "DB_PORT"
          value = var.db_port
        },
        {
          name  = "DB_USER"
          value = var.db_user
        },
        {
          name  = "SENTRY_DSN"
          value = var.sentry_dsn
        },
        {
          name  = "ENABLE_DEV_ENDPOINTS",
          value = tostring(var.enable_dev_endpoints)
        },
        {
          name  = "VIRTUAL_ENV",
          value = "/venv"
        },
        # TODO: move to secrets management
        {
          name  = "DB_PASSWORD"
          value = var.db_password
        },
      ]
      secrets = [
        for k, v in var.env_arn_map : {
          name      = k
          valueFrom = v
        }
      ]
    },
  ])
  tags = var.tags
}

resource "aws_security_group" "task_sg" {
  name        = local.task_sg_name
  description = "Security group for ECS Task"
  vpc_id      = var.vpc_id
  ingress {
    protocol  = "tcp"
    from_port = 8001
    to_port   = 8001
    security_groups = [
      var.lb_sg_id
    ]
  }
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = var.tags
}

resource "aws_ecs_service" "this" {
  name                   = local.service_name
  cluster                = module.ecs.cluster_id
  desired_count          = var.desired_count
  task_definition        = aws_ecs_task_definition.service.arn
  launch_type            = "FARGATE"
  enable_execute_command = true
  network_configuration {
    security_groups = [aws_security_group.task_sg.id]
    subnets         = var.private_subnets
  }
  load_balancer {
    target_group_arn = var.target_group_arn
    container_name   = local.ecs_container_name
    container_port   = 8001
  }
  tags = var.tags
}
