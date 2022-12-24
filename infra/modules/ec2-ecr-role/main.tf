locals {
    full_name = "${var.app_name}-monitoring"
}

resource "aws_iam_policy" "ec2_policy" {
  name        = "${local.full_name}-policy"
  description = "Policy to provide permission for EC2 to have read-only access ECR"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:DescribeImageScanFindings",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetLifecyclePolicy",
            "ecr:GetLifecyclePolicyPreview",
            "ecr:GetRepositoryPolicy",
            "ecr:ListImages",
            "ecr:ListTagsForResource",
        ],
        Resource = var.ecr_arns
      },
      {
        Effect = "Allow",
        Action = concat(
            [
                "ecr:GetAuthorizationToken",
                # TODO: should this be restricted to a specific resource?
                "ssm:GetParametersByPath",
            ],
            var.extra_global_permissions
        ),
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "ec2_role" {
  name = "${local.full_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "ec2_policy_role" {
  name       = "${local.full_name}-policy-attachment"
  roles      = [aws_iam_role.ec2_role.name]
  policy_arn = aws_iam_policy.ec2_policy.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${local.full_name}-profile"
  role = aws_iam_role.ec2_role.name
}