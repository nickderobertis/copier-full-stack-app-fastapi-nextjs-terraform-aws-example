
locals {
  # Create the map by extracting the env name from the full name in module.ssm.arn_map
  # e.g. EMAIL_USER from /stackranked-pr-6/app/EMAIL_USER
  env_arn_map = { for k, v in module.ssm.arn_map : replace(k, "//${var.app_name}/${var.service_name}//", "") => v }
}


module "ssm" {
  source  = "cloudposse/ssm-parameter-store/aws//."
  version = "0.10.0"
  parameter_write = concat(
    [
      for k, v in var.secrets : {
        name        = "/${var.app_name}/${var.service_name}/${k}"
        type        = "SecureString"
        value       = v
        overwrite   = "true"
        description = "Secret parameter ${k} for ${var.app_name}"
      }
    ],
    [
      for k, v in var.params : {
        name        = "/${var.app_name}/${var.service_name}/${k}"
        type        = "String"
        value       = v
        overwrite   = "true"
        description = "Parameter ${k} for ${var.app_name}"
      }
    ]
  )

  tags = var.tags
}
