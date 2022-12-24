module "zones" {
  source  = "terraform-aws-modules/route53/aws//modules/zones"
  version = "2.9.0"

  zones = {
    "${var.main_domain}" = {
      comment       = "${var.main_domain} (production)"
      force_destroy = true
      tags          = var.tags
    }
  }
}
