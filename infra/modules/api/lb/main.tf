locals {
  log_bucket_name = "${var.app_name}-lb-logs"
}

module "lb" {
  source  = "terraform-aws-modules/alb/aws//."
  version = "7.0.0"

  name               = "${var.app_name}-alb"
  load_balancer_type = "application"

  vpc_id          = var.vpc_id
  subnets         = var.public_subnets
  security_groups = [var.security_group_id]

  access_logs = {
    bucket = local.log_bucket_name
  }

  target_groups = [
    {
      name_prefix      = "${var.app_short_name}-"
      backend_protocol = "HTTP"
      backend_port     = 8001
      target_type      = "ip"
      health_check = {
        enabled             = true
        interval            = 30
        path                = "/health-check"
        port                = "8001"
        healthy_threshold   = 3
        unhealthy_threshold = 3
        timeout             = 6
        protocol            = "HTTP"
        matcher             = "200"
      }
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      certificate_arn    = var.acm_certificate_arn
      target_group_index = 0
    }
  ]

  http_tcp_listeners = [
    {
      port               = 80
      protocol           = "HTTP"
      target_group_index = 0
    }
  ]

  tags = var.tags
}


resource "aws_s3_bucket" "this" {
  bucket        = local.log_bucket_name
  force_destroy = true
  tags          = var.tags
}

resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.this.id
  acl    = "private"
}

resource "aws_s3_bucket_policy" "this" {
  bucket = aws_s3_bucket.this.id
  policy = data.aws_iam_policy_document.s3_bucket_lb_write.json
}

data "aws_elb_service_account" "main" {}

data "aws_iam_policy_document" "s3_bucket_lb_write" {
  policy_id = "s3_bucket_lb_logs"

  statement {
    actions = [
      "s3:PutObject",
    ]
    effect = "Allow"
    resources = [
      "${aws_s3_bucket.this.arn}/*",
    ]

    principals {
      identifiers = ["${data.aws_elb_service_account.main.arn}"]
      type        = "AWS"
    }
  }

  statement {
    actions = [
      "s3:PutObject"
    ]
    effect    = "Allow"
    resources = ["${aws_s3_bucket.this.arn}/*"]
    principals {
      identifiers = ["delivery.logs.amazonaws.com"]
      type        = "Service"
    }
  }


  statement {
    actions = [
      "s3:GetBucketAcl"
    ]
    effect    = "Allow"
    resources = ["${aws_s3_bucket.this.arn}"]
    principals {
      identifiers = ["delivery.logs.amazonaws.com"]
      type        = "Service"
    }
  }
}
